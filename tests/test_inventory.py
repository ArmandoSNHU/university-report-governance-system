import json
import tempfile
import unittest
from pathlib import Path

from argos_bridge.inventory import (
    load_report_assets,
    render_markdown_catalog,
    summarize_assets,
    validate_report_assets,
)


class InventoryTests(unittest.TestCase):
    def test_loads_report_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            path.write_text(
                json.dumps(
                    {
                        "report_id": "STU-001",
                        "name": "Active Registration",
                        "functional_area": "Student",
                        "sql_file": "sql_queries/student.sql",
                        "sensitivity": "FERPA",
                        "parameters": ["term_code"],
                        "output_type": "dashboard",
                        "audience": "Student Services",
                        "business_question": "How many students are active?",
                    }
                ),
                encoding="utf-8",
            )

            assets = load_report_assets(tmp)

        self.assertEqual(1, len(assets))
        self.assertEqual("Student", assets[0].functional_area)
        self.assertEqual(["term_code"], assets[0].parameters)
        self.assertEqual("dashboard", assets[0].output_type)

    def test_summarizes_assets(self):
        assets = load_report_assets("reports")

        summary = summarize_assets(assets)

        self.assertGreaterEqual(summary["total_reports"], 5)
        self.assertIn("Student", summary["by_area"])
        self.assertGreaterEqual(summary["parameterized_reports"], 4)

    def test_report_metadata_references_existing_sql(self):
        assets = load_report_assets("reports")

        issues = validate_report_assets(assets)

        self.assertEqual([], issues)

    def test_catalog_contains_deans_report(self):
        assets = load_report_assets("reports")

        catalog = render_markdown_catalog(assets)

        self.assertIn("# Report Catalog", catalog)
        self.assertIn("AA-001", catalog)
        self.assertIn("Dean's Academic Performance Summary", catalog)


if __name__ == "__main__":
    unittest.main()
