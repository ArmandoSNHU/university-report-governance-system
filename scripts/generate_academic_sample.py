from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "academic_sample"
SQL_PATH = ROOT / "sql_queries" / "seed_academic_data.sql"
REPORT_PATH = ROOT / "docs" / "deans_report.md"

GRADE_POINTS = {
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
}

PROFESSORS = [
    (501, "Elena", "Martinez", "Computer Science"),
    (502, "Marcus", "Reed", "Business"),
    (503, "Priya", "Shah", "Biology"),
    (504, "Daniel", "Kim", "Mathematics"),
    (505, "Nadia", "Hernandez", "Nursing"),
    (506, "Owen", "Brooks", "Criminal Justice"),
    (507, "Sophia", "Nguyen", "English"),
    (508, "Caleb", "Johnson", "History"),
    (509, "Maya", "Patel", "Psychology"),
    (510, "Victor", "Santos", "Accounting"),
]

COURSES = [
    (301, "CSCI-1301", "Introduction to Programming", 3, 501),
    (302, "BUSI-2301", "Principles of Management", 3, 502),
    (303, "BIOL-1406", "General Biology I", 4, 503),
    (304, "MATH-1314", "College Algebra", 3, 504),
    (305, "NURS-1201", "Foundations of Nursing", 2, 505),
    (306, "CRIJ-1301", "Introduction to Criminal Justice", 3, 506),
    (307, "ENGL-1301", "Composition I", 3, 507),
    (308, "HIST-1302", "United States History II", 3, 508),
    (309, "PSYC-2301", "General Psychology", 3, 509),
    (310, "ACCT-2301", "Financial Accounting", 3, 510),
]

STUDENTS = [
    (1001, "Ariana", "Lopez", "Computer Science", ["A", "A-", "B+", "A"]),
    (1002, "Mateo", "Garcia", "Business", ["B+", "B", "A-", "B+"]),
    (1003, "Isabella", "Ramirez", "Biology", ["A", "B+", "A-", "B"]),
    (1004, "Noah", "Flores", "Mathematics", ["B", "B+", "B", "A-"]),
    (1005, "Sofia", "Torres", "Nursing", ["A-", "B+", "B+", "A"]),
    (1006, "Liam", "Cruz", "Criminal Justice", ["B", "B-", "B+", "B"]),
    (1007, "Camila", "Rivera", "English", ["A", "A", "A-", "B+"]),
    (1008, "Ethan", "Morales", "History", ["B+", "B+", "B", "B-"]),
    (1009, "Mia", "Castillo", "Psychology", ["A-", "B+", "A", "A-"]),
    (1010, "Lucas", "Vega", "Accounting", ["B", "B+", "A-", "B+"]),
    (1011, "Valeria", "Sanchez", "Computer Science", ["A", "B+", "B+", "A-"]),
    (1012, "Benjamin", "Ortiz", "Business", ["C+", "B", "B-", "B"]),
    (1013, "Emma", "Gutierrez", "Biology", ["B+", "A-", "B+", "B+"]),
    (1014, "Sebastian", "Ramos", "Mathematics", ["B", "C+", "B", "B+"]),
    (1015, "Olivia", "Mendoza", "Nursing", ["A-", "A", "B+", "A"]),
    (1016, "Diego", "Herrera", "Criminal Justice", ["B-", "B", "C+", "B"]),
    (1017, "Natalia", "Silva", "English", ["A", "A-", "A", "A"]),
    (1018, "James", "Reyes", "History", ["B+", "B", "B-", "C+"]),
    (1019, "Elena", "Navarro", "Psychology", ["A-", "A-", "B+", "A"]),
    (1020, "Samuel", "Pena", "Accounting", ["B", "B", "B+", "B"]),
    (1021, "Lucia", "Delgado", "Computer Science", ["A-", "B+", "A-", "B+"]),
    (1022, "Adrian", "Campos", "Business", ["B+", "B", "C+", "B-"]),
    (1023, "Victoria", "Medina", "Biology", ["A", "A-", "A-", "B+"]),
    (1024, "Julian", "Aguilar", "Mathematics", ["B", "B+", "B+", "B"]),
    (1025, "Gabriela", "Fuentes", "Nursing", ["A", "A-", "B+", "A-"]),
    (1026, "Henry", "Salazar", "Criminal Justice", ["C+", "B-", "B", "B"]),
    (1027, "Daniela", "Cabrera", "English", ["A-", "A", "A-", "B+"]),
    (1028, "Leo", "Dominguez", "History", ["B", "B-", "C+", "B"]),
    (1029, "Renata", "Ibarra", "Psychology", ["A", "B+", "A", "A-"]),
    (1030, "Isaac", "Valdez", "Accounting", ["B+", "B+", "B", "A-"]),
]

COURSE_ROTATION = [301, 302, 303, 304, 305, 306, 307, 308, 309, 310]
MAJOR_CHART_ORDER = [
    ("Computer Science", "CS"),
    ("Business", "Business"),
    ("Biology", "Biology"),
    ("Mathematics", "Math"),
    ("Nursing", "Nursing"),
    ("Criminal Justice", "CJ"),
    ("English", "English"),
    ("History", "History"),
    ("Psychology", "Psych"),
    ("Accounting", "Acct"),
]


def calculate_gpa(grades: list[str]) -> float:
    return round(sum(GRADE_POINTS[grade] for grade in grades) / len(grades), 2)


def build_students() -> list[dict[str, object]]:
    rows = []
    for student_id, first_name, last_name, major, grades in STUDENTS:
        rows.append(
            {
                "student_id": student_id,
                "first_name": first_name,
                "last_name": last_name,
                "major": major,
                "gpa": f"{calculate_gpa(grades):.2f}",
            }
        )
    return rows


def build_enrollments() -> list[dict[str, object]]:
    rows = []
    enrollment_id = 9001
    for offset, (student_id, _, _, _, grades) in enumerate(STUDENTS):
        course_ids = [COURSE_ROTATION[(offset + step) % len(COURSE_ROTATION)] for step in range(4)]
        for course_id, grade in zip(course_ids, grades):
            rows.append(
                {
                    "enrollment_id": enrollment_id,
                    "student_id": student_id,
                    "course_id": course_id,
                    "term_code": "SPRING2026",
                    "grade": grade,
                    "grade_points": f"{GRADE_POINTS[grade]:.1f}",
                    "pass_flag": "Y",
                }
            )
            enrollment_id += 1
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def sql_value(value: object) -> str:
    if isinstance(value, int):
        return str(value)
    return "'" + str(value).replace("'", "''") + "'"


def write_sql(students: list[dict[str, object]], enrollments: list[dict[str, object]]) -> None:
    lines = [
        "-- Fictional academic sample data for University Report Governance System",
        "-- All records are made up and safe for public demonstration.",
        "",
        "INSERT INTO SC_ERP.PROFESSORS (professor_id, first_name, last_name, department_name) VALUES",
    ]
    professor_values = [
        f"({professor_id}, {sql_value(first_name)}, {sql_value(last_name)}, {sql_value(department)})"
        for professor_id, first_name, last_name, department in PROFESSORS
    ]
    lines.append(",\n".join(professor_values) + ";")

    lines.extend(["", "INSERT INTO SC_ERP.COURSES (course_id, course_code, course_title, credit_hours, professor_id) VALUES"])
    course_values = [
        f"({course_id}, {sql_value(code)}, {sql_value(title)}, {credits}, {professor_id})"
        for course_id, code, title, credits, professor_id in COURSES
    ]
    lines.append(",\n".join(course_values) + ";")

    lines.extend(["", "INSERT INTO SC_ERP.STUDENT_ACADEMIC_SUMMARY (student_id, first_name, last_name, major, gpa) VALUES"])
    student_values = [
        "("
        + ", ".join(
            [
                str(row["student_id"]),
                sql_value(row["first_name"]),
                sql_value(row["last_name"]),
                sql_value(row["major"]),
                str(row["gpa"]),
            ]
        )
        + ")"
        for row in students
    ]
    lines.append(",\n".join(student_values) + ";")

    lines.extend(["", "INSERT INTO SC_ERP.STUDENT_COURSE_GRADES (enrollment_id, student_id, course_id, term_code, grade, grade_points, pass_flag) VALUES"])
    enrollment_values = [
        "("
        + ", ".join(
            [
                str(row["enrollment_id"]),
                str(row["student_id"]),
                str(row["course_id"]),
                sql_value(row["term_code"]),
                sql_value(row["grade"]),
                str(row["grade_points"]),
                sql_value(row["pass_flag"]),
            ]
        )
        + ")"
        for row in enrollments
    ]
    lines.append(",\n".join(enrollment_values) + ";")
    SQL_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_deans_report(students: list[dict[str, object]], enrollments: list[dict[str, object]]) -> None:
    major_counts = Counter(str(row["major"]) for row in students)
    grade_counts = Counter(str(row["grade"]) for row in enrollments)
    major_gpas: dict[str, list[float]] = defaultdict(list)
    for row in students:
        major_gpas[str(row["major"])].append(float(row["gpa"]))

    overall_gpa = round(sum(float(row["gpa"]) for row in students) / len(students), 2)
    top_students = sorted(students, key=lambda row: float(row["gpa"]), reverse=True)[:5]

    lines = [
        "# Dean's Academic Performance Report",
        "",
        "This report summarizes fictional Spring 2026 academic sample data for University Report Governance System. All students, professors, courses, and grades are made up for demonstration purposes.",
        "",
        "## Executive Summary",
        "",
        f"- Students reviewed: {len(students)}",
        f"- Courses represented: {len(COURSES)}",
        f"- Professors represented: {len(PROFESSORS)}",
        f"- Course enrollments reviewed: {len(enrollments)}",
        f"- Overall GPA: {overall_gpa:.2f}",
        "- Grade outcome: all recorded grades are passing.",
        "",
        "## GPA By Major",
        "",
        "```mermaid",
        "xychart-beta",
        "    title \"Average GPA by Major\"",
        "    x-axis [" + ", ".join(f"\"{label}\"" for _, label in MAJOR_CHART_ORDER) + "]",
        "    y-axis \"GPA\" 2.0 --> 4.0",
        "    bar ["
        + ", ".join(f"{sum(major_gpas[major]) / len(major_gpas[major]):.2f}" for major, _ in MAJOR_CHART_ORDER)
        + "]",
        "```",
        "",
        "## Grade Distribution",
        "",
        "```mermaid",
        "pie showData",
        "    title Passing Grade Distribution",
    ]
    for grade in ["A", "A-", "B+", "B", "B-", "C+"]:
        lines.append(f"    \"{grade}\" : {grade_counts[grade]}")
    lines.extend(
        [
            "```",
            "",
            "## Enrollment By Major",
            "",
            "| Major | Students | Average GPA |",
            "| --- | ---: | ---: |",
        ]
    )
    for major, count in sorted(major_counts.items()):
        avg_gpa = sum(major_gpas[major]) / len(major_gpas[major])
        lines.append(f"| {major} | {count} | {avg_gpa:.2f} |")

    lines.extend(
        [
            "",
            "## Top GPA Students",
            "",
            "| Student ID | Student | Major | GPA |",
            "| ---: | --- | --- | ---: |",
        ]
    )
    for row in top_students:
        lines.append(
            f"| {row['student_id']} | {row['first_name']} {row['last_name']} | {row['major']} | {row['gpa']} |"
        )

    lines.extend(
        [
            "",
            "## Notes For Report Review",
            "",
            "- GPA is calculated from the four recorded course grades per student.",
            "- All grades map to passing grade points from `C+` through `A`.",
            "- This report is safe for public demonstration because it contains no real student data.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    students = build_students()
    enrollments = build_enrollments()
    professors = [
        {
            "professor_id": professor_id,
            "first_name": first_name,
            "last_name": last_name,
            "department_name": department,
        }
        for professor_id, first_name, last_name, department in PROFESSORS
    ]
    courses = [
        {
            "course_id": course_id,
            "course_code": code,
            "course_title": title,
            "credit_hours": credits,
            "professor_id": professor_id,
        }
        for course_id, code, title, credits, professor_id in COURSES
    ]

    write_csv(DATA_DIR / "students.csv", students)
    write_csv(DATA_DIR / "professors.csv", professors)
    write_csv(DATA_DIR / "courses.csv", courses)
    write_csv(DATA_DIR / "grades.csv", enrollments)
    write_sql(students, enrollments)
    write_deans_report(students, enrollments)

    print(f"Wrote academic sample data to {DATA_DIR}")
    print(f"Wrote SQL seed file to {SQL_PATH}")
    print(f"Wrote dean's report to {REPORT_PATH}")


if __name__ == "__main__":
    main()
