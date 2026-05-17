# University Report Governance System Codex Guide

## Project Purpose

University Report Governance System is a standard-library Python project for demonstrating Banner-style institutional reporting and Argos-style report governance. Its workflow is:

1. Parse text-based reporting exports.
2. Extract embedded SQL statements.
3. Save extracted SQL under `sql_queries/`.
4. Maintain report metadata under `reports/`.
5. Validate SQL for safety and maintainability.
6. Summarize report assets through a CLI inventory.

The repo uses fictional `SC_ERP` sample objects and does not connect to a real Banner, Argos, or ERP environment.

## Repository Layout

- `argos_bridge/` - package with CLI, extraction, validation, and inventory logic.
- `reports/` - JSON metadata that models Argos-style report definitions.
- `sql_queries/` - sample SQL report assets and generated extracts.
- `docs/architecture.md` - current architecture overview.
- `docs/architechture.md` - legacy architecture note kept because the file already existed.
- `scripts/` - compatibility wrappers plus sample data generation.
- `tests/` - Python `unittest` coverage.
- `sample_export.txt` - sample text export used by the extractor.

## Common Commands

Run from the repository root:

```powershell
python -m argos_bridge demo
python -m argos_bridge inventory
python -m argos_bridge validate sql_queries
python -m argos_bridge catalog
python -m argos_bridge extract sample_export.txt
python -m unittest discover
```

There is no runtime dependency manifest beyond the standard library. `pyproject.toml` only describes the package.

## Coding Notes

- Keep the project standard-library-only unless a real need appears.
- Avoid personal preparation notes in the repo; public docs should stay project-focused.
- Be careful when running `scripts/seed_data.py`; it rewrites `sql_queries/seed_sample_data.sql` with randomized content.
- Be careful when running `extract`; it creates timestamped SQL files in `sql_queries/`.
- If validation gets stricter, run it against all existing SQL files and update tests.
- If report metadata fields change, update `argos_bridge/inventory.py`, sample JSON files, and tests together.

## Verification

Use this baseline before handing off changes:

```powershell
python -m unittest discover
python -m argos_bridge inventory
python -m argos_bridge validate sql_queries
python -m argos_bridge catalog
python -m argos_bridge demo
```

Warnings are acceptable when they identify intentionally preserved legacy extracts, but errors should be fixed.

## Known Gaps

- SQL extraction is regex-based and intentionally lightweight.
- Metadata simulates Argos-style governance; it is not a proprietary Argos export parser.
- Existing generated SQL extracts are checked in, so repeated extraction can add duplicate timestamped files.
- The future ERP API push step is not implemented.
