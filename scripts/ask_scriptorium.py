import argparse
import json
import math
import re
import subprocess
import urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"
OUTPUT_LOG_PATH = ROOT / "outputs" / "generated" / "legacy" / "ask_scriptorium_runs.md"

DEFAULT_EMBEDDING_MODEL = "embeddinggemma"
DEFAULT_LLM_MODEL = "llama3.2:1b"

OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"

TOP_K = 5
K1 = 1.5
B = 0.75

BM25_WEIGHT = 0.5
VECTOR_WEIGHT = 0.5

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "could", "did",
    "do", "does", "for", "from", "had", "has", "have", "he", "her", "his",
    "how", "in", "is", "it", "its", "of", "on", "or", "our", "she", "the",
    "their", "this", "to", "was", "we", "were", "what", "when", "where",
    "whether", "which", "who", "why", "with", "would",
    "about", "answer", "based", "selected", "chunks", "work",
    "boethius", "philosophy"
}

ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def load_chunks() -> list[dict]:
    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data["chunks"]


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

        documents.append({
            "chunk": chunk,
            "terms": terms,
            "term_counts": term_counts,
            "length": len(terms),
        })

    doc_count = len(documents)
    avg_doc_length = sum(doc["length"] for doc in documents) / doc_count

    document_frequency = Counter()

    for doc in documents:
        for term in set(doc["terms"]):
            document_frequency[term] += 1

    idf = {}

    for term, df in document_frequency.items():
        idf[term] = math.log(1 + ((doc_count - df + 0.5) / (df + 0.5)))

    return {
        "documents": documents,
        "avg_doc_length": avg_doc_length,
        "idf": idf,
    }


def bm25_score(query_terms: list[str], doc: dict, index: dict) -> float:
    score = 0.0
    doc_length = doc["length"]
    avg_doc_length = index["avg_doc_length"]

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
# Embeddings / vector search
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

    with urllib.request.urlopen(request, timeout=300) as response:
        data = json.loads(response.read().decode("utf-8"))

    embeddings = data.get("embeddings")

    if not embeddings:
        raise RuntimeError(f"No embeddings returned by Ollama. Response: {data}")

    return embeddings


def get_embedding_cache_path(model: str) -> Path:
    safe_model_name = model.replace(":", "_").replace("/", "_")
    return ROOT / "outputs" / "generated" / "embeddings" / f"chunk_embeddings_{safe_model_name}.json"


def get_chunk_embeddings(model: str, chunks: list[dict]) -> list[list[float]]:
    cache_path = get_embedding_cache_path(model)
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]

    if cache_path.exists():
        cache = json.loads(cache_path.read_text(encoding="utf-8"))

        if cache.get("model") == model and cache.get("chunk_ids") == chunk_ids:
            print(f"Using cached chunk embeddings: {cache_path}")
            return cache["embeddings"]

    print("Creating chunk embeddings. This may take a minute...")
    chunk_texts = [chunk["text"] for chunk in chunks]
    embeddings = call_ollama_embed(model, chunk_texts)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            {
                "model": model,
                "chunk_ids": chunk_ids,
                "embeddings": embeddings,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print(f"Saved chunk embeddings to: {cache_path}")
    return embeddings


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
# Hybrid retrieval
# ----------------------------

def normalize_scores(scores: dict[str, float]) -> dict[str, float]:
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


def retrieve_hybrid(
    question: str,
    chunks: list[dict],
    bm25_index: dict,
    chunk_embeddings: list[list[float]],
    embedding_model: str,
    top_k: int,
) -> list[dict]:
    bm25_scores = calculate_bm25_scores(question, bm25_index)

    question_embedding = call_ollama_embed(embedding_model, [question])[0]
    vector_scores = calculate_vector_scores(question_embedding, chunks, chunk_embeddings)

    normalized_bm25 = normalize_scores(bm25_scores)
    normalized_vector = normalize_scores(vector_scores)

    chunks_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}
    results = []

    for chunk_id in chunks_by_id:
        bm25_norm = normalized_bm25.get(chunk_id, 0.0)
        vector_norm = normalized_vector.get(chunk_id, 0.0)

        hybrid_score = (BM25_WEIGHT * bm25_norm) + (VECTOR_WEIGHT * vector_norm)

        chunk = chunks_by_id[chunk_id]

        results.append({
            "chunk_id": chunk_id,
            "hybrid_score": hybrid_score,
            "bm25_norm": bm25_norm,
            "vector_norm": vector_norm,
            "start_line": chunk["start_line"],
            "end_line": chunk["end_line"],
            "word_count": chunk["word_count"],
            "text": chunk["text"],
        })

    results.sort(key=lambda item: item["hybrid_score"], reverse=True)
    return results[:top_k]


# ----------------------------
# Answer generation
# ----------------------------

def clean_model_output(text: str) -> str:
    text = ANSI_ESCAPE_RE.sub("", text)
    text = text.replace("\r", "")
    return text.strip()


def run_ollama(model: str, prompt: str) -> str:
    commands_to_try = [
        ["ollama", "run", "--nowordwrap", model],
        ["ollama", "run", model],
    ]

    last_error = None

    for command in commands_to_try:
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            timeout=300,
        )

        if result.returncode == 0:
            return clean_model_output(result.stdout)

        last_error = (
            f"Command failed: {' '.join(command)}\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

        if "--nowordwrap" in command:
            continue

    raise RuntimeError(f"Ollama failed.\n\n{last_error}")


def build_grounded_prompt(question: str, retrieved_chunks: list[dict]) -> str:
    chunk_blocks = []

    for chunk in retrieved_chunks:
        chunk_blocks.append(
            f"""[{chunk["chunk_id"]}]
Lines: {chunk["start_line"]}-{chunk["end_line"]}

{chunk["text"]}"""
        )

    chunks_text = "\n\n---\n\n".join(chunk_blocks)

    return f"""You are Local Scriptorium, a source-grounded research assistant.

Use ONLY the supplied source chunks to answer the question.

Rules:
- Cite chunk IDs for claims.
- Do not use outside knowledge.
- If the chunks are insufficient, say what cannot be determined from the supplied chunks.
- Do not pretend the source says more than it says.
- Be concise but specific.

Question:
{question}

Supplied source chunks:

{chunks_text}

Answer:
"""


def append_log(
    question: str,
    retrieved_chunks: list[dict],
    answer: str,
    embedding_model: str,
    llm_model: str,
) -> None:
    OUTPUT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "",
        "---",
        "",
        f"## Run: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Embedding model: `{embedding_model}`",
        "",
        f"LLM model: `{llm_model}`",
        "",
        "### Question",
        "",
        question,
        "",
        "### Retrieved Chunks",
        "",
    ]

    for chunk in retrieved_chunks:
        lines.append(
            f"- `{chunk['chunk_id']}` — hybrid {chunk['hybrid_score']:.3f} "
            f"| BM25 norm {chunk['bm25_norm']:.3f} "
            f"| vector norm {chunk['vector_norm']:.3f}"
        )

    lines.extend([
        "",
        "### Answer",
        "",
        "```text",
        answer,
        "```",
        "",
    ])

    with OUTPUT_LOG_PATH.open("a", encoding="utf-8") as file:
        file.write("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question", help="Question to ask Local Scriptorium")
    parser.add_argument("--top-k", type=int, default=TOP_K)
    parser.add_argument("--embedding-model", default=DEFAULT_EMBEDDING_MODEL)
    parser.add_argument("--llm-model", default=DEFAULT_LLM_MODEL)
    parser.add_argument("--no-log", action="store_true")

    args = parser.parse_args()

    chunks = load_chunks()
    bm25_index = build_bm25_index(chunks)
    chunk_embeddings = get_chunk_embeddings(args.embedding_model, chunks)

    retrieved_chunks = retrieve_hybrid(
        question=args.question,
        chunks=chunks,
        bm25_index=bm25_index,
        chunk_embeddings=chunk_embeddings,
        embedding_model=args.embedding_model,
        top_k=args.top_k,
    )

    print()
    print("Retrieved chunks:")
    for chunk in retrieved_chunks:
        print(
            f"- {chunk['chunk_id']} | hybrid={chunk['hybrid_score']:.3f} "
            f"| BM25={chunk['bm25_norm']:.3f} "
            f"| vector={chunk['vector_norm']:.3f} "
            f"| lines {chunk['start_line']}-{chunk['end_line']}"
        )

    prompt = build_grounded_prompt(args.question, retrieved_chunks)

    print()
    print("Answer:")
    print()

    answer = run_ollama(args.llm_model, prompt)
    print(answer)

    if not args.no_log:
        append_log(
            question=args.question,
            retrieved_chunks=retrieved_chunks,
            answer=answer,
            embedding_model=args.embedding_model,
            llm_model=args.llm_model,
        )
        print()
        print(f"Logged run to: {OUTPUT_LOG_PATH}")


if __name__ == "__main__":
    main()
