import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

QUESTIONS_PATH = ROOT / "evals" / "manual_rag_questions.md"
CHUNK_MAP_PATH = ROOT / "evals" / "manual_rag_chunk_map.md"
CHUNKS_PATH = ROOT / "chunks" / "boethius_consolation_chunks.json"
OUTPUT_PATH = ROOT / "outputs" / "manual_rag_prompt_test.md"

DEFAULT_MODEL = "llama3.2:1b"
DEFAULT_QUESTIONS = ["Q01", "Q03", "Q09"]

ANSI_ESCAPE_RE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")


def read_text(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    return path.read_text(encoding="utf-8")


def clean_model_output(text: str) -> str:
    """
    Remove terminal control sequences from captured Ollama output.

    Some Ollama CLI output can include cursor-movement / line-clearing codes
    when captured by a script. These show up as ugly strings like:
    ESC[2D ESC[K

    This function strips those artifacts before writing Markdown.
    """
    text = ANSI_ESCAPE_RE.sub("", text)
    text = text.replace("\r", "")
    return text.strip()


def load_chunks() -> dict:
    with CHUNKS_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return {chunk["chunk_id"]: chunk for chunk in data["chunks"]}


def extract_question(question_id: str, questions_md: str) -> str:
    """
    Extract question text from evals/manual_rag_questions.md.

    Looks for a section like:

    ### Q01: ...
    Question:
    ...
    Question type:
    """
    pattern = rf"### {question_id}:.*?Question:\s*(.*?)\s*Question type:"
    match = re.search(pattern, questions_md, flags=re.DOTALL)

    if not match:
        raise ValueError(f"Could not find question text for {question_id}")

    return match.group(1).strip()


def extract_candidate_chunk_ids(question_id: str, chunk_map_md: str) -> list[str]:
    """
    Extract candidate chunk IDs from evals/manual_rag_chunk_map.md.

    Looks inside the question section and finds IDs like:
    BOETHIUS_CONSOLATION_001_CHUNK_011
    """
    section_pattern = rf"## {question_id}:.*?(?=\n## Q\d\d:|\n# Findings|\Z)"
    section_match = re.search(section_pattern, chunk_map_md, flags=re.DOTALL)

    if not section_match:
        raise ValueError(f"Could not find chunk map section for {question_id}")

    section_text = section_match.group(0)

    chunk_ids = re.findall(
        r"BOETHIUS_CONSOLATION_001_CHUNK_\d{3}",
        section_text,
    )

    unique_chunk_ids = []
    for chunk_id in chunk_ids:
        if chunk_id not in unique_chunk_ids:
            unique_chunk_ids.append(chunk_id)

    if not unique_chunk_ids:
        raise ValueError(f"No candidate chunk IDs found for {question_id}")

    return unique_chunk_ids


def build_ungrounded_prompt(question_id: str, question: str) -> str:
    return f"""You are answering a question about Boethius.

Do not use source chunks. Answer from your own knowledge only.

Question ID: {question_id}

Question:
{question}

Answer in 4-8 sentences.
If you are unsure, say so.
"""


def build_grounded_prompt(
    question_id: str,
    question: str,
    candidate_chunk_ids: list[str],
    chunks_by_id: dict,
) -> str:
    chunk_blocks = []

    for chunk_id in candidate_chunk_ids:
        chunk = chunks_by_id.get(chunk_id)

        if not chunk:
            raise ValueError(f"Chunk ID not found in chunk JSON: {chunk_id}")

        chunk_blocks.append(
            f"""[{chunk_id}]
Lines: {chunk["start_line"]}-{chunk["end_line"]}
Words: {chunk["word_count"]}

{chunk["text"]}"""
        )

    chunks_text = "\n\n---\n\n".join(chunk_blocks)

    return f"""You are a source-grounded research assistant.

Use ONLY the supplied source chunks to answer the question.

Rules:
- Cite chunk IDs for claims.
- Do not use outside knowledge.
- If the chunks are insufficient, say what cannot be determined from the supplied chunks.
- Do not pretend the source says more than it says.
- Keep the answer concise but specific.

Question ID: {question_id}

Question:
{question}

Supplied source chunks:

{chunks_text}

Answer:
"""


def run_ollama(model: str, prompt: str) -> str:
    """
    Run the prompt through Ollama using stdin.

    First tries --nowordwrap to avoid terminal cursor-control artifacts.
    If the local Ollama version does not support that flag, it falls back
    to normal ollama run and still cleans captured output.
    """
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
            timeout=180,
        )

        if result.returncode == 0:
            return clean_model_output(result.stdout)

        last_error = (
            f"Command failed: {' '.join(command)}\n\n"
            f"STDOUT:\n{result.stdout}\n\n"
            f"STDERR:\n{result.stderr}"
        )

        # If --nowordwrap is unsupported, try the fallback command.
        if "--nowordwrap" in command:
            continue

    raise RuntimeError(f"Ollama failed.\n\n{last_error}")


def append_result_block(
    output_lines: list[str],
    question_id: str,
    question: str,
    candidate_chunk_ids: list[str],
    ungrounded_answer: str,
    grounded_answer: str,
) -> None:
    output_lines.extend(
        [
            f"## {question_id}",
            "",
            "### Question",
            "",
            question,
            "",
            "### Candidate Chunks Used for Grounded Prompt",
            "",
        ]
    )

    for chunk_id in candidate_chunk_ids:
        output_lines.append(f"- `{chunk_id}`")

    output_lines.extend(
        [
            "",
            "### Ungrounded Local Model Answer",
            "",
            "```text",
            ungrounded_answer,
            "```",
            "",
            "### Grounded Local Model Answer",
            "",
            "```text",
            grounded_answer,
            "```",
            "",
            "### Comparison Notes",
            "",
            "TODO: Did the grounded answer improve accuracy, specificity, caution, and citation behavior?",
            "",
            "### Grounding Issues",
            "",
            "TODO: Did the model cite unsupported claims, ignore chunks, or use outside knowledge?",
            "",
            "---",
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model name. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--questions",
        nargs="+",
        default=DEFAULT_QUESTIONS,
        help="Question IDs to test, e.g. Q01 Q03 Q09",
    )

    args = parser.parse_args()

    questions_md = read_text(QUESTIONS_PATH)
    chunk_map_md = read_text(CHUNK_MAP_PATH)
    chunks_by_id = load_chunks()

    output_lines = [
        "# Manual RAG Prompt Test",
        "",
        f"Date: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"Local model: `{args.model}`",
        "",
        "## Goal",
        "",
        "Compare local model answers with and without supplied source chunks.",
        "",
        "This tests whether grounded prompts improve answer quality and whether the model follows source-use rules.",
        "",
        "---",
        "",
    ]

    for question_id in args.questions:
        print(f"Running {question_id}...")

        question = extract_question(question_id, questions_md)
        candidate_chunk_ids = extract_candidate_chunk_ids(question_id, chunk_map_md)

        print(f"  Candidate chunks: {', '.join(candidate_chunk_ids)}")

        ungrounded_prompt = build_ungrounded_prompt(question_id, question)
        grounded_prompt = build_grounded_prompt(
            question_id,
            question,
            candidate_chunk_ids,
            chunks_by_id,
        )

        print("  Running ungrounded prompt...")
        ungrounded_answer = run_ollama(args.model, ungrounded_prompt)

        print("  Running grounded prompt...")
        grounded_answer = run_ollama(args.model, grounded_prompt)

        append_result_block(
            output_lines=output_lines,
            question_id=question_id,
            question=question,
            candidate_chunk_ids=candidate_chunk_ids,
            ungrounded_answer=ungrounded_answer,
            grounded_answer=grounded_answer,
        )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text("\n".join(output_lines), encoding="utf-8")

    print()
    print("Manual RAG prompt test complete.")
    print(f"Output written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()