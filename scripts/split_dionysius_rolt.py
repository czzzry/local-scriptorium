"""Split the approved 1920 Rolt scan OCR into its two treatises."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sources_public/raw/pseudo_dionysius_rolt.txt"


def write(path: Path, source_id: str, title: str, body: str) -> None:
    header = ("---\n"
              f"source_id: {source_id}\n"
              f"title: {title}\n"
              "author: Pseudo-Dionysius\n"
              "translator: C. E. Rolt\n"
              "source_type: primary_text_translation\n"
              "status: cleaned_for_v0.3\n"
              "---\n\n")
    path.write_text(header + body.strip() + "\n", encoding="utf-8")


def main() -> None:
    lines = RAW.read_text(encoding="utf-8", errors="replace").splitlines()
    divine_start = next(i for i, line in enumerate(lines) if line.strip().replace(" ", "") == "CHAPTERI" and i > 2400)
    mystical_start = next(i for i, line in enumerate(lines) if "THE    MYSTICAL   THEOLOGY" in line and i > 9000)
    write(ROOT / "sources_public/processed/pseudo_dionysius_divine_names_rolt_clean.md", "PSEUDO_DIONYSIUS_DIVINE_NAMES_001", "The Divine Names", "\n".join(lines[divine_start:mystical_start]))
    write(ROOT / "sources_public/processed/pseudo_dionysius_mystical_theology_rolt_clean.md", "PSEUDO_DIONYSIUS_MYSTICAL_THEOLOGY_001", "The Mystical Theology", "\n".join(lines[mystical_start:]))


if __name__ == "__main__":
    main()
