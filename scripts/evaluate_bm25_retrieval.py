import json
import math
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_PATH = ROOT / "evals" / "manual_rag_questions.md"
CHUNK_MAP_PATH = ROOT / "evals" / "manual_rag_chunk_map.md"
CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"
OUTPUT_PATH = ROOT / "outputs" / "generated" / "legacy" / "bm25_retrieval_eval.md"

TOP_K = 5

# BM25 tuning constants.
# k1 controls term-frequency saturation.
# b controls document-length normalization.
K1 = 1.5
B = 0.75

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


def build_bm25_index(chunks: list[dict]) -> dict:
    """
    Build a simple in-memory BM25 index.

    This is not a production search engine. It is a local retrieval baseline.
    """
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
        # Standard BM25-style IDF with smoothing.
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


def retrieve_bm25(question: str, index: dict, top_k: int = TOP_K) -> list[dict]:
    query_terms = tokenize(question)
    results = []

    for doc in index["documents"]:
        score = bm25_score(query_terms, doc, index)

        if score <= 0:
            continue

        chunk = doc["chunk"]

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


def note_for_result(recall: float, precision: float, max_possible_recall: float) -> str:
    if recall == 1.0:
        return (
            "Strong result. BM25 retrieved all manually expected chunks in the top 5. "
            "This suggests lexical retrieval is sufficient for this question."
        )

    if recall >= 0.5:
        return (
            "Partial-to-good result. BM25 retrieved a meaningful portion of the manually expected evidence, "
            "but did not fully reproduce the manual evidence map."
        )

    if recall > 0:
        return (
            "Weak-to-partial result. BM25 retrieved some expected evidence, but missed most of the manual evidence map."
        )

    return (
        "Weak result. BM25 retrieved none of the manually expected chunks in the top 5. "
        "This suggests lexical retrieval is not enough for this question."
    )


def main() -> None:
    questions_md = read_text(QUESTIONS_PATH)
    chunk_map_md = read_text(CHUNK_MAP_PATH)
    chunks = load_chunks()

    questions = extract_questions(questions_md)
    index = build_bm25_index(chunks)

    output = [
        "# BM25 Retrieval Evaluation",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Top K: {TOP_K}",
        "",
        f"BM25 parameters: k1={K1}, b={B}",
        "",
        "## Goal",
        "",
        "Evaluate a BM25 lexical retrieval baseline against the manual RAG chunk map.",
        "",
        "This is a retrieval test, not an answer-generation test.",
        "",
        "BM25 is a stronger lexical baseline than raw keyword counting because it accounts for term rarity, term frequency saturation, and document length.",
        "",
        "---",
        "",
    ]

    recalls = []
    precisions = []

    for question_id, question in questions.items():
        expected = extract_expected_chunks(question_id, chunk_map_md)
        retrieved_items = retrieve_bm25(question, index, TOP_K)
        retrieved_ids = [item["chunk_id"] for item in retrieved_items]

        metrics = calculate_metrics(expected, retrieved_ids)

        recalls.append(metrics["recall"])
        precisions.append(metrics["precision"])

        query_terms = tokenize(question)

        output.extend(
            [
                f"## {question_id}",
                "",
                "### Question",
                "",
                question,
                "",
                "### Query Terms",
                "",
                "`" + "`, `".join(query_terms) + "`" if query_terms else "_No query terms after stopword filtering._",
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

        if retrieved_items:
            for item in retrieved_items:
                marker = "HIT" if item["chunk_id"] in expected else "MISS"
                output.extend(
                    [
                        f"- `{item['chunk_id']}` — BM25 score {item['score']:.3f} — {marker}",
                        f"  - lines {item['start_line']}-{item['end_line']}, {item['word_count']} words",
                        f"  - preview: {item['preview']}",
                    ]
                )
        else:
            output.append("- No chunks retrieved")

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
                note_for_result(
                    metrics["recall"],
                    metrics["precision"],
                    metrics["max_possible_recall"],
                ),
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
            "BM25 provides a stronger lexical retrieval baseline than raw keyword counting.",
            "",
            "A high Recall@5 would mean the retriever usually gets the manually expected evidence into the model context. A low Recall@5 means the retriever is missing expected evidence and should not be trusted as the final retrieval method.",
            "",
            "Precision@5 helps identify how much extra noise appears in the retrieved context. Recall asks whether the right chunks were found; precision asks how much of the retrieved set was actually expected evidence.",
            "",
            "## Decision",
            "",
            "Use BM25 as the serious lexical baseline for the MVP. Compare it against the earlier simple keyword-count baseline. If BM25 still performs poorly on interpretive questions, the next retrieval improvement should be semantic or hybrid retrieval.",
            "",
        ]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(output), encoding="utf-8")

    print("BM25 retrieval evaluation complete.")
    print(f"Output written to: {OUTPUT_PATH}")
    print(f"Average Recall@{TOP_K}: {average_recall:.2f}")
    print(f"Average Precision@{TOP_K}: {average_precision:.2f}")


if __name__ == "__main__":
    main()
