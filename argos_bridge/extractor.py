from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

SQL_PATTERN = re.compile(
    r"\b(SELECT|INSERT|UPDATE)\b[\s\S]*?;",
    re.IGNORECASE,
)


def extract_sql(input_file: str | Path) -> list[str]:
    """Extract SQL statements from a text export."""
    path = Path(input_file)
    data = path.read_text(encoding="utf-8")
    return [match.group(0).strip() for match in SQL_PATTERN.finditer(data)]


def save_queries(
    queries: list[str],
    output_dir: str | Path = "sql_queries",
    timestamp: str | None = None,
) -> list[Path]:
    """Save extracted SQL statements and return the created paths."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = timestamp or datetime.now().strftime("%Y%m%d_%H%M")
    saved_paths: list[Path] = []

    for index, query in enumerate(queries):
        path = out_dir / f"extracted_query_{stamp}_{index}.sql"
        path.write_text(
            "-- Extracted via University Report Governance System\n" + query.strip() + "\n",
            encoding="utf-8",
        )
        saved_paths.append(path)

    return saved_paths
