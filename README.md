# University Report Governance System

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Tests](https://github.com/ArmandoSNHU/university-report-governance-system/actions/workflows/ci.yml/badge.svg)](https://github.com/ArmandoSNHU/university-report-governance-system/actions/workflows/ci.yml)
[![Dependencies](https://img.shields.io/badge/dependencies-standard%20library-green)](#requirements)

University Report Governance System is a Python command-line project for Banner-style institutional reporting and Argos-style report governance. It demonstrates how report SQL can be extracted, documented, inventoried, and validated before it is treated as a governed reporting asset.

The project uses fictional `SC_ERP` sample objects. It does not connect to a real Banner, Argos, Ellucian, Evisions, or ERP environment.

## Table Of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [CLI Reference](#cli-reference)
- [Academic Sample Dataset](#academic-sample-dataset)
- [Report Asset Model](#report-asset-model)
- [Validation Rules](#validation-rules)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)

## Overview

Institutional reporting often depends on three pieces working together:

1. Source-system data, such as Banner-style student, finance, HR, and financial aid records.
2. SQL report logic that answers operational business questions.
3. A governed reporting layer that documents audience, parameters, sensitivity, and output expectations.

University Report Governance System models that workflow locally. SQL files represent report logic, JSON files represent Argos-style report metadata, and the CLI provides repeatable commands for inventory and validation.

## Features

- Extracts SQL statements from text-based report exports.
- Maintains governed sample reports for Student, Finance, Human Resources, Financial Aid, and Academic Affairs.
- Tracks report metadata including audience, parameters, output type, sensitivity, and business question.
- Validates SQL for risky or weak reporting patterns.
- Provides a report inventory summary by functional area and sensitivity.
- Uses only the Python standard library.
- Includes unit tests and GitHub Actions CI.

## Quick Start

Clone the repository and run the demo:

```powershell
git clone https://github.com/ArmandoSNHU/university-report-governance-system.git
cd university-report-governance-system
python -m argos_bridge demo
```

Expected result:

```text
University Report Governance System demo
========================================
Report inventory: 5 report(s)
Parameterized reports: 4

Checked 12 SQL file(s).
All SQL files pass University Report Governance System standards.
```

## Requirements

- Python 3.10 or newer
- No third-party runtime dependencies

Optional editable install:

```powershell
python -m pip install -e .
```

## CLI Reference

Run all commands from the repository root.

### Demo

Runs inventory and validation together:

```powershell
python -m argos_bridge demo
```

### Inventory

Summarizes report metadata from `reports/`:

```powershell
python -m argos_bridge inventory
```

### Catalog

Generates `docs/report_catalog.md` from report metadata:

```powershell
python -m argos_bridge catalog
```

### Validate

Validates SQL files in `sql_queries/`:

```powershell
python -m argos_bridge validate sql_queries
```

### Extract

Extracts SQL statements from a text export and writes timestamped `.sql` files:

```powershell
python -m argos_bridge extract sample_export.txt
```

Generated files are written to `sql_queries/`. Review generated files before committing them.

## Academic Sample Dataset

The repository includes a fictional academic sample dataset under `data/academic_sample/`:

- 30 made-up students
- 10 made-up professors
- 10 courses
- 120 passing grade records
- Student GPAs calculated from course grades

The dean-facing summary is available in `docs/deans_report.md`. It includes GitHub-rendered Mermaid charts for GPA by major and passing grade distribution.

The governed report catalog is available in `docs/report_catalog.md`.

## Report Asset Model

Each governed report has two parts:

- A SQL file in `sql_queries/`
- A metadata file in `reports/`

Example metadata:

```json
{
  "report_id": "STU-001",
  "name": "Active Registration by Department",
  "functional_area": "Student",
  "sql_file": "sql_queries/student_active_registration.sql",
  "sensitivity": "FERPA - aggregated",
  "parameters": ["term_code"],
  "output_type": "dashboard",
  "audience": "Student Services and academic leadership",
  "business_question": "How many active students and credit hours are registered by department for a selected term?"
}
```

Current sample report areas:

| Area | Report |
| --- | --- |
| Student | Active Registration by Department |
| Finance | Outstanding Student Balances |
| Human Resources | Active Positions by Department |
| Financial Aid | Financial Aid Missing Requirements |
| Academic Affairs | Dean's Academic Performance Summary |

## Validation Rules

The validator currently checks for:

- Dangerous or inappropriate commands: `DROP TABLE`, `TRUNCATE`, `DELETE FROM`, `ALTER TABLE`
- Missing semicolons
- `SELECT *` usage in governed reports
- SQL files that do not reference the fictional `SC_ERP` sample schema

Errors fail validation. Warnings are reported so report authors can clean up weak patterns before release.

## Project Structure

```text
university-report-governance-system/
├── argos_bridge/       # CLI package
├── docs/               # Architecture notes
├── data/               # Fictional academic sample data
├── reports/            # Argos-style report metadata
├── scripts/            # Compatibility wrappers and sample-data script
├── sql_queries/        # Governed SQL report examples
├── tests/              # Unit tests
├── sample_export.txt   # Sample text export for extraction
└── pyproject.toml      # Package metadata
```

## Testing

Run the full test suite:

```powershell
python -m unittest discover
```

Recommended local verification before committing:

```powershell
python -m unittest discover
python -m argos_bridge validate sql_queries
python -m argos_bridge catalog
python -m argos_bridge demo
```

## Roadmap

- Add metadata-to-SQL consistency checks.
- Add richer SQL parsing for comments, multiline statements, and vendor-specific syntax.
- Add report catalog export to Markdown or HTML.
- Add optional JSON output for CLI commands.
- Add support for comparing report versions across Git commits.

## Disclaimer

University Report Governance System is a learning and demonstration project. All schema names, report names, and data examples are fictional. This repository does not include proprietary Argos exports, Banner configuration, production data, credentials, or integrations with real institutional systems.
