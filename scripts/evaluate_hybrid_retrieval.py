import argparse
import json
import math
import re
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_PATH = ROOT / "evals" / "manual_rag_questions.md"
CHUNK_MAP_PATH = ROOT / "evals" / "manual_rag_chunk_map.md"
CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"
OUTPUT_PATH = ROOT / "outputs" / "generated" / "legacy" / "hybrid_retrieval_eval.md"

DEFAULT_MODEL = "embeddinggemma"
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"

TOP_K = 5
BATCH_SIZE = 8

# BM25 defaults
K1 = 1.5
B = 0.75

# Hybrid defaults
DEFAULT_BM25_WEIGHT = 0.5
DEFAULT_VECTOR_WEIGHT = 0.5

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "could", "did",
    "do", "does", "for", "from", "had", "has", "have", "he", "her", "his",
    "how", "in", "is", "it", "its", "of", "on", "or", "our", "she", "the",
    "their", "this", "to", "was", "we", "were", "what", "when", "where",
    "whether", "which", "who", "why", "with", "would",

    # Question/task words that are usually not useful retrieval terms.
    "about", "answer", "argue", "based", "beginning", "cannot", "claim",
    "describe", "identify", "own", "provide", "rather", "safe", "safely",
    "say", "selected", "sense", "than", "work",

    # Corpus-wide terms that are often too broad in this project.
    "boethius", "chunks", "philosophy"
}


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


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z']+", text.lower())

    terms = []
    for word in words:
        word = word.strip("'")

        if len(word) < 3:
            continue

        if word in STOPWORDS:
            continue

        terms.append(word)

    return terms


# ----------------------------
# BM25
# ----------------------------

def build_bm25_index(chunks: list[dict]) -> dict:
    documents = []

    for chunk in chunks:
        terms = tokenize(chunk["text"])
        term_counts = Counter(terms)

        documents.append(
            {
                "chunk": chunk,
                "terms": terms,
                "term_counts": term_counts,
                "length": len(terms),
            }
        )

    doc_count = len(documents)
    avg_doc_length = (
        sum(doc["length"] for doc in documents) / doc_count if doc_count else 0
    )

    document_frequency = Counter()

    for doc in documents:
        for term in set(doc["terms"]):
            document_frequency[term] += 1

    idf = {}

    for term, df in document_frequency.items():
        idf[term] = math.log(1 + ((doc_count - df + 0.5) / (df + 0.5)))

    return {
        "documents": documents,
        "doc_count": doc_count,
        "avg_doc_length": avg_doc_length,
        "idf": idf,
    }


def bm25_score(query_terms: list[str], doc: dict, index: dict) -> float:
    score = 0.0
    doc_length = doc["length"]
    avg_doc_length = index["avg_doc_length"] or 1

    for term in query_terms:
        if term not in doc["term_counts"]:
            continue

        tf = doc["term_counts"][term]
        term_idf = index["idf"].get(term, 0.0)

        numerator = tf * (K1 + 1)
        denominator = tf + K1 * (1 - B + B * (doc_length / avg_doc_length))

        score += term_idf * (numerator / denominator)

    return score


def calculate_bm25_scores(question: str, index: dict) -> dict[str, float]:
    query_terms = tokenize(question)
    scores = {}

    for doc in index["documents"]:
        chunk_id = doc["chunk"]["chunk_id"]
        scores[chunk_id] = bm25_score(query_terms, doc, index)

    return scores


# ----------------------------
# Vector embeddings
# ----------------------------

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


def calculate_vector_scores(
    question_embedding: list[float],
    chunks: list[dict],
    chunk_embeddings: list[list[float]],
) -> dict[str, float]:
    scores = {}

    for chunk, embedding in zip(chunks, chunk_embeddings):
        scores[chunk["chunk_id"]] = cosine_similarity(question_embedding, embedding)

    return scores


# ----------------------------
# Hybrid scoring
# ----------------------------

def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
    """
    Normalize a score dictionary to 0-1 using min-max normalization.

    This lets us combine BM25 scores and cosine scores, which live on
    different scales.
    """
    values = list(scores.values())

    if not values:
        return {}

    min_score = min(values)
    max_score = max(values)

    if max_score == min_score:
        return {key: 0.0 for key in scores}

    return {
        key: (value - min_score) / (max_score - min_score)
        for key, value in scores.items()
    }


def calculate_hybrid_scores(
    bm25_scores: dict[str, float],
    vector_scores: dict[str, float],
    bm25_weight: float,
    vector_weight: float,
) -> dict[str, dict]:
    normalized_bm25 = normalize_scores(bm25_scores)
    normalized_vector = normalize_scores(vector_scores)

    hybrid = {}

    all_chunk_ids = set(bm25_scores) | set(vector_scores)

    for chunk_id in all_chunk_ids:
        bm25_norm = normalized_bm25.get(chunk_id, 0.0)
        vector_norm = normalized_vector.get(chunk_id, 0.0)

        hybrid_score = (bm25_weight * bm25_norm) + (vector_weight * vector_norm)

        hybrid[chunk_id] = {
            "hybrid_score": hybrid_score,
            "bm25_raw": bm25_scores.get(chunk_id, 0.0),
            "bm25_norm": bm25_norm,
            "vector_raw": vector_scores.get(chunk_id, 0.0),
            "vector_norm": vector_norm,
        }

    return hybrid


def retrieve_hybrid(
    chunks: list[dict],
    hybrid_scores: dict[str, dict],
    top_k: int = TOP_K,
) -> list[dict]:
    chunks_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}

    ranked = sorted(
        hybrid_scores.items(),
        key=lambda item: item[1]["hybrid_score"],
        reverse=True,
    )

    results = []

    for chunk_id, scores in ranked[:top_k]:
        chunk = chunks_by_id[chunk_id]

        results.append(
            {
                "chunk_id": chunk_id,
                "hybrid_score": scores["hybrid_score"],
                "bm25_raw": scores["bm25_raw"],
                "bm25_norm": scores["bm25_norm"],
                "vector_raw": scores["vector_raw"],
                "vector_norm": scores["vector_norm"],
                "start_line": chunk["start_line"],
                "end_line": chunk["end_line"],
                "word_count": chunk["word_count"],
                "preview": chunk["text"][:500].replace("\n", " "),
            }
        )

    return results


# ----------------------------
# Evaluation
# ----------------------------

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


def note_for_result(recall: float, precision: float) -> str:
    if recall == 1.0:
        return (
            "Strong result. Hybrid retrieval found all manually expected chunks in the top 5."
        )

    if recall >= 0.5:
        return (
            "Partial-to-good result. Hybrid retrieval found a meaningful portion of the expected evidence, "
            "but did not fully reproduce the manual evidence map."
        )

    if recall > 0:
        return (
            "Weak-to-partial result. Hybrid retrieval found some expected evidence, but missed most of the manual map."
        )

    return (
        "Weak result. Hybrid retrieval found none of the manually expected chunks in the top 5."
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama embedding model. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--bm25-weight",
        type=float,
        default=DEFAULT_BM25_WEIGHT,
        help=f"BM25 weight. Default: {DEFAULT_BM25_WEIGHT}",
    )
    parser.add_argument(
        "--vector-weight",
        type=float,
        default=DEFAULT_VECTOR_WEIGHT,
        help=f"Vector weight. Default: {DEFAULT_VECTOR_WEIGHT}",
    )

    args = parser.parse_args()

    total_weight = args.bm25_weight + args.vector_weight
    if total_weight == 0:
        raise ValueError("BM25 weight and vector weight cannot both be zero.")

    bm25_weight = args.bm25_weight / total_weight
    vector_weight = args.vector_weight / total_weight

    questions_md = read_text(QUESTIONS_PATH)
    chunk_map_md = read_text(CHUNK_MAP_PATH)
    chunks = load_chunks()
    questions = extract_questions(questions_md)

    print(f"Using embedding model: {args.model}")
    print(f"Hybrid weights: BM25={bm25_weight:.2f}, vector={vector_weight:.2f}")
    print(f"Loaded {len(chunks)} chunks.")

    print("Building BM25 index...")
    bm25_index = build_bm25_index(chunks)

    print("Creating chunk embeddings...")
    chunk_texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = embed_in_batches(args.model, chunk_texts)

    question_ids = list(questions.keys())
    question_texts = [questions[qid] for qid in question_ids]

    print("Creating question embeddings...")
    question_embeddings = embed_in_batches(args.model, question_texts)

    output = [
        "# Hybrid Retrieval Evaluation",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Embedding model: `{args.model}`",
        "",
        f"Top K: {TOP_K}",
        "",
        f"Hybrid weights: BM25={bm25_weight:.2f}, vector={vector_weight:.2f}",
        "",
        f"BM25 parameters: k1={K1}, b={B}",
        "",
        "## Goal",
        "",
        "Evaluate a hybrid retrieval baseline against the manual RAG chunk map.",
        "",
        "Hybrid retrieval combines BM25 lexical retrieval with vector / embedding retrieval.",
        "",
        "This is a retrieval test, not an answer-generation test.",
        "",
        "---",
        "",
    ]

    recalls = []
    precisions = []

    for question_id, question, question_embedding in zip(
        question_ids, question_texts, question_embeddings
    ):
        expected = extract_expected_chunks(question_id, chunk_map_md)

        bm25_scores = calculate_bm25_scores(question, bm25_index)
        vector_scores = calculate_vector_scores(question_embedding, chunks, chunk_embeddings)

        hybrid_scores = calculate_hybrid_scores(
            bm25_scores=bm25_scores,
            vector_scores=vector_scores,
            bm25_weight=bm25_weight,
            vector_weight=vector_weight,
        )

        retrieved_items = retrieve_hybrid(chunks, hybrid_scores, TOP_K)
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
                    (
                        f"- `{item['chunk_id']}` — hybrid {item['hybrid_score']:.3f} — {marker}"
                        f" | BM25 raw {item['bm25_raw']:.3f}, BM25 norm {item['bm25_norm']:.3f}"
                        f" | vector raw {item['vector_raw']:.4f}, vector norm {item['vector_norm']:.3f}"
                    ),
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
                note_for_result(metrics["recall"], metrics["precision"]),
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
            "Hybrid retrieval combines exact-word lexical matching with semantic vector similarity.",
            "",
            "A strong hybrid result would suggest that BM25 and vector retrieval complement each other. A weak hybrid result would suggest that weighting, query design, chunk quality, or the manual evidence map need further review.",
            "",
            "The default weights are intentionally simple: 50 percent BM25 and 50 percent vector. This avoids tuning the result to a tiny eval set.",
            "",
            "## Decision",
            "",
            "Compare this result against the keyword, BM25, and vector baselines. Use the comparison to decide which retrieval method is strongest for the MVP.",
            "",
        ]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(output), encoding="utf-8")

    print()
    print("Hybrid retrieval evaluation complete.")
    print(f"Output written to: {OUTPUT_PATH}")
    print(f"Average Recall@{TOP_K}: {average_recall:.2f}")
    print(f"Average Precision@{TOP_K}: {average_precision:.2f}")


if __name__ == "__main__":
    main()
