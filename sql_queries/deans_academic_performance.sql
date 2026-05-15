-- REPORT: Dean's Academic Performance Summary
-- AREA: Academic Affairs
-- PURPOSE: Summarizes fictional course performance by major for dean-level review.
-- PARAMETERS: :term_code
-- SENSITIVITY: FERPA - aggregated academic data

WITH student_term_gpa AS (
    SELECT
        stu.student_id,
        stu.major,
        AVG(grd.grade_points) AS term_gpa
    FROM SC_ERP.STUDENT_ACADEMIC_SUMMARY stu
    JOIN SC_ERP.STUDENT_COURSE_GRADES grd
      ON stu.student_id = grd.student_id
    WHERE grd.term_code = :term_code
      AND grd.pass_flag = 'Y'
    GROUP BY stu.student_id, stu.major
)
SELECT
    major,
    COUNT(student_id) AS students_reviewed,
    ROUND(AVG(term_gpa), 2) AS average_gpa,
    MIN(term_gpa) AS lowest_student_gpa,
    MAX(term_gpa) AS highest_student_gpa
FROM student_term_gpa
GROUP BY major
ORDER BY major;
