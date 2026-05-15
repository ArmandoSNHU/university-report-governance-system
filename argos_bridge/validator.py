from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DANGEROUS_PHRASES = (
    "DROP TABLE",
    "TRUNCATE",
    "DELETE FROM",
    "ALTER TABLE",
)


@dataclass(frozen=True)
class ValidationIssue:
    filename: str
    severity: str
    message: str


@dataclass(frozen=True)
class ValidationReport:
    checked_files: int
    issues: list[ValidationIssue]

    @property
    def passed(self) -> bool:
        return not any(issue.severity == "ERROR" for issue in self.issues)


def validate_sql_file(path: str | Path) -> list[ValidationIssue]:
    sql_path = Path(path)
    content = sql_path.read_text(encoding="utf-8")
    normalized = content.upper()
    issues: list[ValidationIssue] = []

    for phrase in DANGEROUS_PHRASES:
        if phrase in normalized:
            issues.append(
                ValidationIssue(
                    sql_path.name,
                    "ERROR",
                    f"Risky SQL command found: {phrase}",
                )
            )

    if ";" not in content:
        issues.append(
            ValidationIssue(sql_path.name, "ERROR", "SQL statement is missing a semicolon")
        )

    if "SELECT *" in normalized:
        issues.append(
            ValidationIssue(
                sql_path.name,
                "WARNING",
                "Avoid SELECT * in governed reports; list required columns explicitly",
            )
        )

    if " SC_ERP." not in normalized and "SC_ERP." not in normalized:
        issues.append(
            ValidationIssue(
                sql_path.name,
                "WARNING",
                "Report does not reference the sample Banner-style SC_ERP schema",
            )
        )

    return issues


def validate_sql_standards(directory: str | Path) -> ValidationReport:
    root = Path(directory)
    sql_files = sorted(root.glob("*.sql"))
    issues: list[ValidationIssue] = []

    for sql_file in sql_files:
        issues.extend(validate_sql_file(sql_file))

    return ValidationReport(checked_files=len(sql_files), issues=issues)


def format_validation_report(report: ValidationReport) -> str:
    lines = [f"Checked {report.checked_files} SQL file(s)."]

    if not report.issues:
        lines.append("All SQL files pass University Report Governance System standards.")
        return "\n".join(lines)

    for issue in report.issues:
        lines.append(f"{issue.severity}: {issue.filename}: {issue.message}")

    if report.passed:
        lines.append("Validation passed with warnings.")
    else:
        lines.append("Validation failed. Review errors before release.")

    return "\n".join(lines)
