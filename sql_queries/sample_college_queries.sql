-- PROJECT: University Report Governance System
-- SCHEMA: SC_ERP (Sample College ERP)

/* USE CASE: Enrollment Reporting
   DESCRIPTION: Identifies student registration trends across departments.
*/
SELECT 
    dept.department_name, 
    count(stu.id) AS total_students,
    sum(enr.credit_hours) AS fte_credits
FROM SC_ERP.STUDENTS stu
JOIN SC_ERP.ENROLLMENT enr ON stu.id = enr.student_id
JOIN SC_ERP.DEPARTMENTS dept ON enr.dept_id = dept.id
WHERE enr.academic_term = 'SPRING2026'
GROUP BY dept.department_name;

/* USE CASE: Security Audit
   DESCRIPTION: Reports users with elevated database privileges.
*/
SELECT username, role, last_login_date 
FROM SC_ERP.SYSTEM_SECURITY 
WHERE access_level = 'ADMIN' 
  AND account_status = 'ACTIVE';

/* USE CASE: Data Integrity Check
   DESCRIPTION: Identifies orphan enrollment records (enrollments without valid students).
   This is used for troubleshooting ERP synchronization issues.
*/
SELECT 
    enr.enrollment_id, 
    enr.student_id, 
    enr.course_id
FROM SC_ERP.ENROLLMENT enr
LEFT JOIN SC_ERP.STUDENTS stu ON enr.student_id = stu.id
WHERE stu.id IS NULL;
