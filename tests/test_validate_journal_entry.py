from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_journal_entry.py"
SPEC = importlib.util.spec_from_file_location("validate_journal_entry", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ValidateEntryTests(unittest.TestCase):
    def test_accepts_balanced_entry(self) -> None:
        entry = {
            "lines": [
                {"debit": "10.00", "credit": "0.00"},
                {"debit": "0.00", "credit": "10.00"},
            ]
        }

        self.assertEqual(MODULE.validate_entry(entry), [])

    def test_rejects_unbalanced_entry(self) -> None:
        entry = {
            "lines": [
                {"debit": "10.00", "credit": "0.00"},
                {"debit": "0.00", "credit": "9.00"},
            ]
        }

        errors = MODULE.validate_entry(entry)

        self.assertTrue(any("unbalanced" in error for error in errors))

    def test_rejects_line_with_debit_and_credit(self) -> None:
        entry = {
            "lines": [
                {"debit": "10.00", "credit": "1.00"},
                {"debit": "0.00", "credit": "9.00"},
            ]
        }

        errors = MODULE.validate_entry(entry)

        self.assertTrue(any("either a debit or a credit" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
