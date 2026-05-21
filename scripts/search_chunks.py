import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"


def load_chunks() -> list[dict]:
    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data["chunks"]


def search_chunks(query: str, chunks: list[dict], limit: int = 10) -> list[dict]:
    terms = [term.lower() for term in query.split() if term.strip()]

    results = []

    for chunk in chunks:
        text_lower = chunk["text"].lower()

        score = sum(text_lower.count(term) for term in terms)

        if score > 0:
            results.append(
                {
                    "score": score,
                    "chunk_id": chunk["chunk_id"],
                    "start_line": chunk["start_line"],
                    "end_line": chunk["end_line"],
                    "word_count": chunk["word_count"],
                    "preview": chunk["text"][:700].replace("\n", " "),
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:limit]


def main() -> None:
    if len(sys.argv) < 2:
        print('Usage: python3 scripts/search_chunks.py "fortune"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    chunks = load_chunks()
    results = search_chunks(query, chunks)

    print(f"Query: {query}")
    print(f"Results: {len(results)}")
    print()

    for item in results:
        print("=" * 80)
        print(f"{item['chunk_id']} | score={item['score']} | lines {item['start_line']}-{item['end_line']} | words={item['word_count']}")
        print()
        print(item["preview"])
        print()


if __name__ == "__main__":
    main()