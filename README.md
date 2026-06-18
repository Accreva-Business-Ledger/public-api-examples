# Accreva public API examples

This repository contains non-production request and response examples for design discussions. Accreva does not publish a general-availability API contract from this repository.

The examples show several rules used in accounting workflows:

- clients submit business intent and line amounts
- servers assign identifiers, entry numbers, actors, and timestamps
- journal entries balance before posting
- approvals remain explicit server-side actions

## Example

`examples/journal-entry-proposal.json` contains a proposed journal entry with decimal amounts encoded as strings.

Validate it with Python 3.11 or later:

```bash
python scripts/validate_journal_entry.py examples/journal-entry-proposal.json
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Safe use

Use placeholder URLs and credentials in derivative examples. Do not publish production endpoints, access tokens, customer records, or internal identifiers.
