from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReportAsset:
    report_id: str
    name: str
    functional_area: str
    sql_file: str
    sensitivity: str
    parameters: list[str]
    business_question: str
    output_type: str
    audience: str


def load_report_assets(metadata_dir: str | Path = "reports") -> list[ReportAsset]:
    root = Path(metadata_dir)
    if not root.exists():
        return []

    assets: list[ReportAsset] = []
    for path in sorted(root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        assets.append(
            ReportAsset(
                report_id=data["report_id"],
                name=data["name"],
                functional_area=data["functional_area"],
                sql_file=data["sql_file"],
                sensitivity=data["sensitivity"],
                parameters=list(data.get("parameters", [])),
                business_question=data["business_question"],
                output_type=data["output_type"],
                audience=data["audience"],
            )
        )
    return assets


def validate_report_assets(
    assets: list[ReportAsset],
    project_root: str | Path = ".",
) -> list[str]:
    root = Path(project_root)
    issues: list[str] = []
    seen_ids: set[str] = set()

    for asset in assets:
        if asset.report_id in seen_ids:
            issues.append(f"Duplicate report_id found: {asset.report_id}")
        seen_ids.add(asset.report_id)

        sql_path = root / asset.sql_file
        if not sql_path.exists():
            issues.append(f"{asset.report_id} references missing SQL file: {asset.sql_file}")

        for field_name in (
            "name",
            "functional_area",
            "sql_file",
            "sensitivity",
            "business_question",
            "output_type",
            "audience",
        ):
            if not getattr(asset, field_name):
                issues.append(f"{asset.report_id} has empty metadata field: {field_name}")

    return issues


def summarize_assets(assets: list[ReportAsset]) -> dict[str, object]:
    by_area: dict[str, int] = {}
    by_sensitivity: dict[str, int] = {}
    parameterized = 0

    for asset in assets:
        by_area[asset.functional_area] = by_area.get(asset.functional_area, 0) + 1
        by_sensitivity[asset.sensitivity] = by_sensitivity.get(asset.sensitivity, 0) + 1
        if asset.parameters:
            parameterized += 1

    return {
        "total_reports": len(assets),
        "by_area": dict(sorted(by_area.items())),
        "by_sensitivity": dict(sorted(by_sensitivity.items())),
        "parameterized_reports": parameterized,
    }


def format_inventory(assets: list[ReportAsset]) -> str:
    if not assets:
        return "No report metadata found."

    summary = summarize_assets(assets)
    lines = [
        f"Report inventory: {summary['total_reports']} report(s)",
        f"Parameterized reports: {summary['parameterized_reports']}",
        "",
        "Functional areas:",
    ]

    for area, count in summary["by_area"].items():
        lines.append(f"- {area}: {count}")

    lines.append("")
    lines.append("Reports:")
    for asset in assets:
        params = ", ".join(asset.parameters) if asset.parameters else "none"
        lines.append(
            f"- {asset.report_id}: {asset.name} "
            f"({asset.functional_area}, {asset.sensitivity}, params: {params})"
        )

    return "\n".join(lines)


def render_markdown_catalog(assets: list[ReportAsset]) -> str:
    summary = summarize_assets(assets)
    lines = [
        "# Report Catalog",
        "",
        "This catalog is generated from the JSON metadata files in `reports/`.",
        "",
        "## Summary",
        "",
        f"- Total reports: {summary['total_reports']}",
        f"- Parameterized reports: {summary['parameterized_reports']}",
        "",
        "## Reports",
        "",
        "| Report ID | Name | Area | Audience | Sensitivity | Parameters | SQL File |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for asset in assets:
        params = ", ".join(asset.parameters) if asset.parameters else "none"
        lines.append(
            "| "
            + " | ".join(
                [
                    asset.report_id,
                    asset.name,
                    asset.functional_area,
                    asset.audience,
                    asset.sensitivity,
                    params,
                    f"`{asset.sql_file}`",
                ]
            )
            + " |"
        )

    lines.extend(["", "## Business Questions", ""])
    for asset in assets:
        lines.append(f"### {asset.report_id}: {asset.name}")
        lines.append("")
        lines.append(asset.business_question)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
