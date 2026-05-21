import json
import re
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_PATH = ROOT / "evals" / "manual_rag_questions.md"
CHUNK_MAP_PATH = ROOT / "evals" / "manual_rag_chunk_map.md"
CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"
OUTPUT_PATH = ROOT / "outputs" / "keyword_retrieval_eval.md"

TOP_K = 5

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "does",
    "for", "from", "how", "in", "is", "it", "of", "on", "or", "the",
    "this", "to", "what", "when", "where", "whether", "which", "who",
    "why", "with", "we", "say", "based", "only", "selected", "chunks",
    "work", "philosophy", "boethius"
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
    """
    Extract question IDs and question text from manual_rag_questions.md.
    """
    pattern = r"### (Q\d\d):.*?Question:\s*(.*?)\s*Question type:"
    matches = re.findall(pattern, questions_md, flags=re.DOTALL)

    if not matches:
        raise ValueError("No questions found.")

    return {qid: question.strip() for qid, question in matches}


def extract_expected_chunks(question_id: str, chunk_map_md: str) -> list[str]:
    """
    Extract manually selected / expected chunk IDs for a question.
    """
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
    """
    Convert text into simple lowercase search terms.
    """
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


def score_chunk(question: str, chunk: dict) -> int:
    """
    Very simple keyword scoring.

    This is intentionally not semantic retrieval. It is a baseline.
    """
    terms = tokenize(question)
    text = chunk["text"].lower()

    score = 0

    for term in terms:
        count = text.count(term)
        score += count

    return score


def retrieve_top_chunks(question: str, chunks: list[dict], top_k: int = TOP_K) -> list[dict]:
    scored = []

    for chunk in chunks:
        score = score_chunk(question, chunk)

        if score > 0:
            scored.append(
                {
                    "score": score,
                    "chunk_id": chunk["chunk_id"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "word_count": chunk["word_count"],
                    "preview": chunk["text"][:500].replace("\n", " "),
                }
            )

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def calculate_overlap(expected: list[str], retrieved: list[str]) -> tuple[list[str], float]:
    if not expected:
        return [], 0.0

    hits = [chunk_id for chunk_id in retrieved if chunk_id in expected]
    recall = len(set(hits)) / len(set(expected))
    return hits, recall


def main() -> None:
    questions_md = read_text(QUESTIONS_PATH)
    chunk_map_md = read_text(CHUNK_MAP_PATH)
    chunks = load_chunks()

    questions = extract_questions(questions_md)

    output = [
        "# Keyword Retrieval Evaluation",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Top K: {TOP_K}",
        "",
        "## Goal",
        "",
        "Evaluate a simple keyword retrieval baseline against the manual RAG chunk map.",
        "",
        "This tests whether a basic keyword search can retrieve the same chunks that were manually selected as relevant evidence.",
        "",
        "This is a retrieval test, not an answer-generation test.",
        "",
        "---",
        "",
    ]

    all_recalls = []

    for question_id, question in questions.items():
        expected = extract_expected_chunks(question_id, chunk_map_md)
        retrieved_items = retrieve_top_chunks(question, chunks, TOP_K)
        retrieved_ids = [item["chunk_id"] for item in retrieved_items]

        hits, recall = calculate_overlap(expected, retrieved_ids)
        all_recalls.append(recall)

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
                "`" + "`, `".join(tokenize(question)) + "`",
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
                        f"- `{item['chunk_id']}` — score {item['score']} — {marker}",
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
                f"Hits: {', '.join(hits) if hits else 'None'}",
                "",
                f"Recall@{TOP_K}: {recall:.2f}",
                "",
                "### Notes",
                "",
                "TODO: Is the retrieval result acceptable? Did keyword search miss relevant evidence? Did it retrieve noisy chunks?",
                "",
                "---",
                "",
            ]
        )

    average_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0.0

    output.extend(
        [
            "# Overall Findings",
            "",
            f"Average Recall@{TOP_K}: {average_recall:.2f}",
            "",
            "## Interpretation",
            "",
            "TODO: Summarize whether keyword retrieval is good enough as a baseline.",
            "",
            "Likely finding: keyword retrieval can find obvious term matches but struggles with conceptual or interpretive questions.",
            "",
            "## Next Step",
            "",
            "TODO: Decide whether to improve keyword retrieval, add semantic retrieval, or move to a stronger model test.",
            "",
        ]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(output), encoding="utf-8")

    print("Keyword retrieval evaluation complete.")
    print(f"Output written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()