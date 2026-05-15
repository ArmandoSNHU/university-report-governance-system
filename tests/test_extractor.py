import tempfile
import unittest
from pathlib import Path

from argos_bridge.extractor import extract_sql, save_queries


class ExtractorTests(unittest.TestCase):
    def test_extracts_multiple_sql_statements(self):
        with tempfile.TemporaryDirectory() as tmp:
            export = Path(tmp) / "export.txt"
            export.write_text(
                "Header\nSELECT id FROM SC_ERP.STUDENTS;\nOther\nupdate SC_ERP.STUDENTS set status = 'A';",
                encoding="utf-8",
            )

            queries = extract_sql(export)

        self.assertEqual(2, len(queries))
        self.assertTrue(queries[0].startswith("SELECT"))
        self.assertTrue(queries[1].lower().startswith("update"))

    def test_save_queries_returns_created_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = save_queries(
                ["SELECT id FROM SC_ERP.STUDENTS;"],
                output_dir=tmp,
                timestamp="20260101_1200",
            )

            self.assertEqual(1, len(paths))
            self.assertTrue(paths[0].exists())
            self.assertIn(
                "-- Extracted via University Report Governance System",
                paths[0].read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
