import copy
import unittest
from pathlib import Path

from local_scriptorium.contracts import (
    ContractError,
    read_json,
    validate_pack,
    validate_source_register,
)


ROOT = Path(__file__).resolve().parents[1]


class SourceRegisterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.register = read_json(ROOT / "sources_public" / "source_register.v2.json")
        self.pack = read_json(ROOT / "data" / "packs" / "late_antiquity_core.v1.json")

    def test_register_and_pack_are_valid(self) -> None:
        validate_source_register(self.register)
        validate_pack(self.pack, self.register)

    def test_blocked_source_cannot_have_processed_path(self) -> None:
        broken = copy.deepcopy(self.register)
        broken["sources"][-1]["processed_path"] = "sources_public/processed/blocked.md"
        with self.assertRaises(ContractError):
            validate_source_register(broken)

    def test_pack_cannot_activate_blocked_source(self) -> None:
        broken = copy.deepcopy(self.pack)
        broken["active_source_ids"].append(broken["blocked_source_ids"][0])
        with self.assertRaises(ContractError):
            validate_pack(broken, self.register)

    def test_pack_cannot_reference_unknown_source(self) -> None:
        broken = copy.deepcopy(self.pack)
        broken["active_source_ids"].append("NOT_IN_REGISTER")
        with self.assertRaises(ContractError):
            validate_pack(broken, self.register)
