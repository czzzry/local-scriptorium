"""Fail CI on common secret, private-data, or machine-path mistakes."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "secret-like value": re.compile(r"(?i)(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]+"),
    "absolute user path": re.compile(r"/(Users|home)/[^/\s]+/"),
    "machine model identifier": re.compile(r"\b(?:MacBookPro|MacBookAir|Macmini|iMac)\d{1,2},\d\b"),
    "operating-system build record": re.compile(r"(?i)BuildVersion\s*[:=]\s*[A-Za-z0-9]+"),
    "private key": re.compile(r"BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY"),
}
ALLOW_SUFFIXES = {".py", ".md", ".json", ".toml", ".yml", ".yaml", ".txt", ".csv"}


def tracked_files() -> list[Path]:
    names = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=ROOT, text=True).splitlines()
    return [
        ROOT / name
        for name in names
        if (ROOT / name).suffix.lower() in ALLOW_SUFFIXES and not name.startswith(".agents/")
    ]


def main() -> int:
    findings = []
    for path in tracked_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if path == Path(__file__).resolve():
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path.relative_to(ROOT)}: {label}")
    if findings:
        print("Privacy check failed:\n" + "\n".join(findings))
        return 1
    print("Privacy and portability check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
