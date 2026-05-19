import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPTS_PATH = ROOT / "evals" / "local_model_baseline_prompts.json"
RUNS_DIR = ROOT / "outputs" / "runs"
OLLAMA_URL = "http://localhost:11434/api/generate"


def safe_filename(value: str) -> str:
    """Convert a model name like llama3.2:1b into a filesystem-safe string."""
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-")


def call_ollama(model: str, prompt: str) -> tuple[str, float]:
    """Send one prompt to the local Ollama server and return the response plus elapsed seconds."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    start = time.time()

    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. Make sure the Ollama app is running."
        ) from exc

    elapsed = time.time() - start
    return result.get("response", "").strip(), elapsed


def load_prompts() -> list[dict]:
    """Load prompt definitions from the JSON prompt file."""
    if not PROMPTS_PATH.exists():
        raise FileNotFoundError(f"Prompt file not found: {PROMPTS_PATH}")

    with PROMPTS_PATH.open("r", encoding="utf-8") as file:
        prompts = json.load(file)

    if not isinstance(prompts, list):
        raise ValueError("Prompt file should contain a JSON list of prompt objects.")

    return prompts


def write_markdown_header(file, model: str) -> None:
    """Write the top section of the Markdown output file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    file.write("# Automated Local Model Baseline Run\n\n")
    file.write("## Goal\n\n")
    file.write(
        "Run the baseline prompt set against the local model using an automated script.\n\n"
    )
    file.write("## Run Metadata\n\n")
    file.write(f"- Date/time: {now}\n")
    file.write(f"- Model: {model}\n")
    file.write("- Local model runner: Ollama\n")
    file.write("- Inference location: local Mac\n")
    file.write("- Prompt source: `evals/local_model_baseline_prompts.json`\n")
    file.write("- Script: `scripts/run_ollama_baseline.py`\n")
    file.write("- No source chunks supplied\n")
    file.write("- No retrieval layer\n")
    file.write("- No RAG\n")
    file.write("- No cloud model used for these answers\n\n")
    file.write("---\n\n")


def main() -> None:
    model = sys.argv[1] if len(sys.argv) > 1 else "llama3.2:1b"

    prompts = load_prompts()
    RUNS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_path = RUNS_DIR / f"local_model_baseline_{timestamp}_{safe_filename(model)}.md"

    print(f"Running {len(prompts)} prompts against model: {model}")
    print(f"Writing output to: {output_path}")

    with output_path.open("w", encoding="utf-8") as file:
        write_markdown_header(file, model)

        for item in prompts:
            prompt_id = item["id"]
            title = item["title"]
            prompt = item["prompt"]

            print(f"Running {prompt_id}: {title}")

            try:
                response, elapsed = call_ollama(model, prompt)
            except Exception as exc:
                response = f"ERROR: {exc}"
                elapsed = 0.0

            file.write(f"## {prompt_id}: {title}\n\n")
            file.write("### Prompt\n\n")
            file.write("```text\n")
            file.write(prompt)
            file.write("\n```\n\n")

            file.write("### Local Model Output\n\n")
            file.write("```text\n")
            file.write(response)
            file.write("\n```\n\n")

            file.write("### Runtime\n\n")
            file.write(f"{elapsed:.2f} seconds\n\n")

            file.write("### Notes\n\n")
            file.write("TODO\n\n")

            file.write("### Usefulness Score\n\n")
            file.write("TODO/5\n\n")

            file.write("---\n\n")

    print("Done.")
    print(output_path)


if __name__ == "__main__":
    main()