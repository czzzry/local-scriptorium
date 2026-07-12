import argparse
import json
import math
import re
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_PATH = ROOT / "evals" / "manual_rag_questions.md"
CHUNK_MAP_PATH = ROOT / "evals" / "manual_rag_chunk_map.md"
CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"
OUTPUT_PATH = ROOT / "outputs" / "generated" / "legacy" / "vector_retrieval_eval.md"

DEFAULT_MODEL = "embeddinggemma"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
TOP_K = 5
BATCH_SIZE = 8


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def load_chunks() -> list[dict]:
    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data["chunks"]


def extract_questions(questions_md: str) -> dict[str, str]:
    pattern = r"### (Q\d\d):.*?Question:\s*(.*?)\s*Question type:"
    matches = re.findall(pattern, questions_md, flags=re.DOTALL)

    if not matches:
        raise ValueError("No questions found in manual_rag_questions.md")

    return {qid: question.strip() for qid, question in matches}


def extract_expected_chunks(question_id: str, chunk_map_md: str) -> list[str]:
    section_pattern = rf"## {question_id}:.*?(?=\n## Q\d\d:|\n# Findings|\Z)"
    section_match = re.search(section_pattern, chunk_map_md, flags=re.DOTALL)

    if not section_match:
        return []

    section_text = section_match.group(0)

    chunk_ids = re.findall(
        r"BOETHIUS_CONSOLATION_001_CHUNK_\d{3}",
        section_text,
    )

    unique = []
    for chunk_id in chunk_ids:
        if chunk_id not in unique:
            unique.append(chunk_id)

    return unique


def call_ollama_embed(model: str, texts: list[str]) -> list[list[float]]:
    payload = {
        "model": model,
        "input": texts,
    }

    request = urllib.request.Request(
        OLLAMA_EMBED_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        raise RuntimeError(
            "Could not call Ollama embeddings API. "
            "Make sure Ollama is running and the embedding model is pulled.\n\n"
            f"Original error: {error}"
        ) from error

    embeddings = data.get("embeddings")

    if not embeddings:
        raise RuntimeError(f"No embeddings returned by Ollama. Response: {data}")

    return embeddings


def embed_in_batches(model: str, texts: list[str]) -> list[list[float]]:
    all_embeddings = []

    for start in range(0, len(texts), BATCH_SIZE):
        end = start + BATCH_SIZE
        batch = texts[start:end]

        print(f"Embedding texts {start + 1}-{min(end, len(texts))} of {len(texts)}...")
        embeddings = call_ollama_embed(model, batch)
        all_embeddings.extend(embeddings)

    return all_embeddings


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot / (norm_a * norm_b)


def retrieve_vector(
    question_embedding: list[float],
    chunk_embeddings: list[list[float]],
    chunks: list[dict],
    top_k: int = TOP_K,
) -> list[dict]:
    results = []

    for chunk, embedding in zip(chunks, chunk_embeddings):
        score = cosine_similarity(question_embedding, embedding)

        results.append(
            {
                "score": score,
                "chunk_id": chunk["chunk_id"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "word_count": chunk["word_count"],
                "preview": chunk["text"][:500].replace("\n", " "),
            }
        )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


def calculate_metrics(expected: list[str], retrieved: list[str]) -> dict:
    expected_set = set(expected)

    hits = [chunk_id for chunk_id in retrieved if chunk_id in expected_set]

    if expected_set:
        recall = len(set(hits)) / len(expected_set)
        max_possible_recall = min(len(expected_set), TOP_K) / len(expected_set)
    else:
        recall = 0.0
        max_possible_recall = 0.0

    precision = len(set(hits)) / TOP_K if TOP_K else 0.0

    return {
        "hits": hits,
        "recall": recall,
        "precision": precision,
        "max_possible_recall": max_possible_recall,
    }


def note_for_result(recall: float) -> str:
    if recall == 1.0:
        return (
            "Strong result. Vector retrieval found all manually expected chunks in the top 5."
        )

    if recall >= 0.5:
        return (
            "Partial-to-good result. Vector retrieval found a meaningful portion of the expected evidence, "
            "but did not fully reproduce the manual evidence map."
        )

    if recall > 0:
        return (
            "Weak-to-partial result. Vector retrieval found some expected evidence, but missed most of the manual map."
        )

    return (
        "Weak result. Vector retrieval found none of the manually expected chunks in the top 5."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama embedding model. Default: {DEFAULT_MODEL}",
    )
    args = parser.parse_args()

    questions_md = read_text(QUESTIONS_PATH)
    chunk_map_md = read_text(CHUNK_MAP_PATH)
    chunks = load_chunks()
    questions = extract_questions(questions_md)

    print(f"Using embedding model: {args.model}")
    print(f"Loaded {len(chunks)} chunks.")
    print("Creating chunk embeddings...")

    chunk_texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = embed_in_batches(args.model, chunk_texts)

    output = [
        "# Vector Retrieval Evaluation",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Embedding model: `{args.model}`",
        "",
        f"Top K: {TOP_K}",
        "",
        "## Goal",
        "",
        "Evaluate a vector / embedding retrieval baseline against the manual RAG chunk map.",
        "",
        "This is a retrieval test, not an answer-generation test.",
        "",
        "Vector retrieval embeds both questions and chunks, then ranks chunks by cosine similarity.",
        "",
        "---",
        "",
    ]

    recalls = []
    precisions = []

    question_ids = list(questions.keys())
    question_texts = [questions[qid] for qid in question_ids]

    print("Creating question embeddings...")
    question_embeddings = embed_in_batches(args.model, question_texts)

    for question_id, question, question_embedding in zip(
        question_ids, question_texts, question_embeddings
    ):
        expected = extract_expected_chunks(question_id, chunk_map_md)
        retrieved_items = retrieve_vector(question_embedding, chunk_embeddings, chunks, TOP_K)
        retrieved_ids = [item["chunk_id"] for item in retrieved_items]

        metrics = calculate_metrics(expected, retrieved_ids)

        recalls.append(metrics["recall"])
        precisions.append(metrics["precision"])

        output.extend(
            [
                f"## {question_id}",
                "",
                "### Question",
                "",
                question,
                "",
                "### Expected Manual Chunks",
                "",
            ]
        )

        if expected:
            for chunk_id in expected:
                output.append(f"- `{chunk_id}`")
        else:
            output.append("- None found in manual map")

        output.extend(
            [
                "",
                f"### Retrieved Top {TOP_K} Chunks",
                "",
            ]
        )

        for item in retrieved_items:
            marker = "HIT" if item["chunk_id"] in expected else "MISS"
            output.extend(
                [
                    f"- `{item['chunk_id']}` — cosine {item['score']:.4f} — {marker}",
                    f"  - lines {item['start_line']}-{item['end_line']}, {item['word_count']} words",
                    f"  - preview: {item['preview']}",
                ]
            )

        output.extend(
            [
                "",
                "### Retrieval Result",
                "",
                f"Hits: {', '.join(metrics['hits']) if metrics['hits'] else 'None'}",
                "",
                f"Recall@{TOP_K}: {metrics['recall']:.2f}",
                "",
                f"Precision@{TOP_K}: {metrics['precision']:.2f}",
                "",
                f"Max possible Recall@{TOP_K} for this question: {metrics['max_possible_recall']:.2f}",
                "",
                "### Notes",
                "",
                note_for_result(metrics["recall"]),
                "",
                "---",
                "",
            ]
        )

    average_recall = sum(recalls) / len(recalls) if recalls else 0.0
    average_precision = sum(precisions) / len(precisions) if precisions else 0.0

    output.extend(
        [
            "# Overall Findings",
            "",
            f"Average Recall@{TOP_K}: {average_recall:.2f}",
            "",
            f"Average Precision@{TOP_K}: {average_precision:.2f}",
            "",
            "## Interpretation",
            "",
            "Vector retrieval is a semantic retrieval baseline. It should perform better than lexical methods when relevant chunks use different wording from the question.",
            "",
            "High Recall@5 means the retriever usually gets expected evidence into the context window. Low Recall@5 means it misses expected evidence and should not be trusted as the final retrieval method.",
            "",
            "## Decision",
            "",
            "Compare this result against the keyword and BM25 baselines. The best MVP retrieval method should be the one that gets the strongest evidence into the top 5 without adding too much noise.",
            "",
        ]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(output), encoding="utf-8")

    print()
    print("Vector retrieval evaluation complete.")
    print(f"Output written to: {OUTPUT_PATH}")
    print(f"Average Recall@{TOP_K}: {average_recall:.2f}")
    print(f"Average Precision@{TOP_K}: {average_precision:.2f}")


if __name__ == "__main__":
    main()
