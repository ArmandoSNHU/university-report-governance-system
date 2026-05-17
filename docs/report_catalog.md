# Report Catalog

This catalog is generated from the JSON metadata files in `reports/`.

## Summary

- Total reports: 5
- Parameterized reports: 4

## Reports

| Report ID | Name | Area | Audience | Sensitivity | Parameters | SQL File |
| --- | --- | --- | --- | --- | --- | --- |
| AA-001 | Dean's Academic Performance Summary | Academic Affairs | Academic Affairs leadership | FERPA - aggregated | term_code | `sql_queries/deans_academic_performance.sql` |
| FIN-001 | Outstanding Student Balances | Finance | Finance staff | FERPA/financial - restricted | minimum_balance | `sql_queries/finance_outstanding_balances.sql` |
| FA-001 | Financial Aid Missing Requirements | Financial Aid | Financial Aid counselors | FERPA/financial aid - restricted | aid_year | `sql_queries/financial_aid_missing_requirements.sql` |
| HR-001 | Active Positions by Department | Human Resources | Human Resources leadership | Employee data - internal | none | `sql_queries/hr_active_positions.sql` |
| STU-001 | Active Registration by Department | Student | Student Services and academic leadership | FERPA - aggregated | term_code | `sql_queries/student_active_registration.sql` |

## Business Questions

### AA-001: Dean's Academic Performance Summary

What is the average passing GPA by major for a selected term?

### FIN-001: Outstanding Student Balances

Which active students have balances above the selected threshold?

### FA-001: Financial Aid Missing Requirements

Which aid applicants still have missing or incomplete requirements for the selected aid year?

### HR-001: Active Positions by Department

How many active employees are assigned to each department by position type?

### STU-001: Active Registration by Department

How many active students and credit hours are registered by department for a selected term?
