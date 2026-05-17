from __future__ import annotations

import argparse
from pathlib import Path

from .extractor import extract_sql, save_queries
from .inventory import (
    format_inventory,
    load_report_assets,
    render_markdown_catalog,
    validate_report_assets,
)
from .validator import format_validation_report, validate_sql_standards


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="argos_bridge",
        description="Extract, inventory, and validate Banner-style SQL report assets.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    extract_parser = subparsers.add_parser("extract", help="Extract SQL from an export file")
    extract_parser.add_argument("input_file", help="Text export containing SQL statements")
    extract_parser.add_argument(
        "--output-dir",
        default="sql_queries",
        help="Directory for extracted SQL files",
    )

    validate_parser = subparsers.add_parser("validate", help="Validate SQL files")
    validate_parser.add_argument("directory", nargs="?", default="sql_queries")

    inventory_parser = subparsers.add_parser("inventory", help="Summarize report metadata")
    inventory_parser.add_argument("metadata_dir", nargs="?", default="reports")

    catalog_parser = subparsers.add_parser("catalog", help="Generate a Markdown report catalog")
    catalog_parser.add_argument(
        "--output",
        default="docs/report_catalog.md",
        help="Path for the generated Markdown catalog",
    )

    subparsers.add_parser("demo", help="Run the project demo checks")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "extract":
        queries = extract_sql(args.input_file)
        if not queries:
            print(f"No SQL statements found in {args.input_file}.")
            return 1
        saved_paths = save_queries(queries, args.output_dir)
        print(f"Extracted {len(saved_paths)} SQL statement(s).")
        for path in saved_paths:
            print(f"Saved: {path}")
        return 0

    if args.command == "validate":
        report = validate_sql_standards(args.directory)
        print(format_validation_report(report))
        return 0 if report.passed else 1

    if args.command == "inventory":
        assets = load_report_assets(args.metadata_dir)
        issues = validate_report_assets(assets)
        print(format_inventory(assets))
        if issues:
            print("")
            print("Metadata issues:")
            for issue in issues:
                print(f"- {issue}")
        return 0 if assets and not issues else 1

    if args.command == "catalog":
        assets = load_report_assets("reports")
        issues = validate_report_assets(assets)
        if issues:
            print("Metadata issues must be fixed before generating the catalog:")
            for issue in issues:
                print(f"- {issue}")
            return 1
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(render_markdown_catalog(assets), encoding="utf-8")
        print(f"Wrote report catalog: {output_path}")
        return 0

    if args.command == "demo":
        print("University Report Governance System demo")
        print("=" * 40)
        assets = load_report_assets("reports")
        issues = validate_report_assets(assets)
        print(format_inventory(assets))
        print("")
        report = validate_sql_standards(Path("sql_queries"))
        print(format_validation_report(report))
        if issues:
            print("")
            print("Metadata issues:")
            for issue in issues:
                print(f"- {issue}")
        return 0 if assets and not issues and report.passed else 1

    return 2
