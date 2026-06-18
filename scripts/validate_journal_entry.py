from __future__ import annotations

import json
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


def validate_entry(entry: object) -> list[str]:
    if not isinstance(entry, dict):
        return ["Entry must be a JSON object."]

    lines = entry.get("lines")
    if not isinstance(lines, list) or len(lines) < 2:
        return ["Entry must contain at least two lines."]

    errors: list[str] = []
    total_debit = Decimal("0.00")
    total_credit = Decimal("0.00")

    for index, line in enumerate(lines, start=1):
        if not isinstance(line, dict):
            errors.append(f"Line {index} must be a JSON object.")
            continue

        try:
            debit = Decimal(str(line.get("debit", "")))
            credit = Decimal(str(line.get("credit", "")))
        except InvalidOperation:
            errors.append(f"Line {index} contains an invalid amount.")
            continue

        if debit < 0 or credit < 0:
            errors.append(f"Line {index} contains a negative amount.")

        if (debit > 0) == (credit > 0):
            errors.append(f"Line {index} must contain either a debit or a credit.")

        total_debit += debit
        total_credit += credit

    if total_debit != total_credit:
        errors.append(
            f"Entry is unbalanced: debit {total_debit} does not equal credit {total_credit}."
        )

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_journal_entry.py PATH")
        return 2

    path = Path(sys.argv[1])
    entry = json.loads(path.read_text(encoding="utf-8"))
    errors = validate_entry(entry)

    if errors:
        for error in errors:
            print(error)
        return 1

    print(f"Valid balanced journal entry: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
