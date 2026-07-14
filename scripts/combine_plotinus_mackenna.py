"""Combine the four original MacKenna volumes covering Enneads I–V."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VOLUMES = [
    (ROOT / "sources_public/raw/plotinus_plotinustranslat01burkuoft.txt", "THE   FIRST   ENNEAD"),
    (ROOT / "sources_public/raw/plotinus_plotinustranslat02burkuoft.txt", "THE   THIRD   ENNEAD"),
    (ROOT / "sources_public/raw/plotinus_plotinustranslat03burkuoft.txt", "THE   FOURTH    ENNEAD"),
    (ROOT / "sources_public/raw/plotinus_plotinustranslat04plotuoft.txt", "THE   FIFTH    ENNEAD"),
]


def locate(lines: list[str], marker: str) -> int:
    compact = "".join(marker.split()).upper()
    candidates = [i for i, line in enumerate(lines) if "".join(line.split()).upper() == compact]
    if not candidates:
        raise ValueError(f"heading not found: {marker}")
    # The first exact heading is the start of the actual Ennead in these scans;
    # contents pages use different spacing or surrounding text.
    return candidates[0]


def main() -> None:
    sections = []
    raw_sections = []
    for path, marker in VOLUMES:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        start = locate(lines, marker)
        sections.append(f"# {marker}\n\n" + "\n".join(lines[start:]).strip())
        raw_sections.append(f"\n\n===== {path.name} =====\n\n" + path.read_text(encoding="utf-8", errors="replace").strip())
    header = ("---\nsource_id: PLOTINUS_ENNEADS_I_V_001\n"
              "title: The Six Enneads, selected Enneads I–V\n"
              "author: Plotinus\ntranslator: Stephen MacKenna\n"
              "source_type: primary_text_translation\nstatus: cleaned_for_v0.3\n---\n\n")
    output = ROOT / "sources_public/processed/plotinus_enneads_i_v_mackenna_clean.md"
    output.write_text(header + "\n\n".join(sections) + "\n", encoding="utf-8")
    (ROOT / "sources_public/raw/plotinus_enneads_i_v_mackenna.txt").write_text("".join(raw_sections) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
