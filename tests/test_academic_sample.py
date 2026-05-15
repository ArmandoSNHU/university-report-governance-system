import csv
import unittest
from pathlib import Path


GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
}


class AcademicSampleTests(unittest.TestCase):
    def setUp(self):
        self.root = Path("data") / "academic_sample"

    def read_csv(self, filename):
        with (self.root / filename).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_dataset_counts(self):
        self.assertEqual(30, len(self.read_csv("students.csv")))
        self.assertEqual(10, len(self.read_csv("courses.csv")))
        self.assertEqual(10, len(self.read_csv("professors.csv")))
        self.assertEqual(120, len(self.read_csv("grades.csv")))

    def test_all_grades_are_passing(self):
        grades = self.read_csv("grades.csv")

        self.assertTrue(all(row["grade"] in GRADE_POINTS for row in grades))
        self.assertTrue(all(row["pass_flag"] == "Y" for row in grades))

    def test_student_gpa_matches_grades(self):
        students = {row["student_id"]: row for row in self.read_csv("students.csv")}
        grades_by_student = {student_id: [] for student_id in students}

        for row in self.read_csv("grades.csv"):
            grades_by_student[row["student_id"]].append(GRADE_POINTS[row["grade"]])

        for student_id, grade_points in grades_by_student.items():
            expected_gpa = round(sum(grade_points) / len(grade_points), 2)
            actual_gpa = float(students[student_id]["gpa"])
            self.assertEqual(expected_gpa, actual_gpa)


if __name__ == "__main__":
    unittest.main()
