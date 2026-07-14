"""Explicit corpus-pack resolution for v0.3 while preserving the v0.2 default."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .contracts import (
    ContractError,
    read_json,
    validate_pack,
    validate_source_register,
)


@dataclass(frozen=True)
class CorpusPack:
    root: Path
    manifest_path: Path
    register_path: Path
    manifest: dict
    source_register: dict

    @property
    def pack_id(self) -> str:
        return self.manifest["pack_id"]

    @property
    def output_root(self) -> Path:
        return self.root / "outputs" / "generated" / "packs" / self.pack_id

    @property
    def corpus_path(self) -> Path:
        return self.output_root / "corpus.v1.json"

    @property
    def questions_path(self) -> Path:
        return self.root / "data" / "evaluation" / "late-antiquity-questions-v2.json"


def load_corpus_pack(root: Path, pack_id: str) -> CorpusPack:
    """Find and validate a pack by its declared pack_id, not by filename convention."""
    register_path = root / "sources_public" / "source_register.v2.json"
    register = read_json(register_path)
    validate_source_register(register)

    matches: list[Path] = []
    for candidate in sorted((root / "data" / "packs").glob("*.json")):
        manifest = read_json(candidate)
        if manifest.get("pack_id") == pack_id:
            matches.append(candidate)
    if len(matches) != 1:
        raise ContractError(f"expected exactly one pack with pack_id {pack_id!r}")

    manifest_path = matches[0]
    manifest = read_json(manifest_path)
    validate_pack(manifest, register)
    return CorpusPack(
        root=root,
        manifest_path=manifest_path,
        register_path=register_path,
        manifest=manifest,
        source_register=register,
    )
