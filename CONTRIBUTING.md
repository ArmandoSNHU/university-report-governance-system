# Contributing

Thank you for improving University Report Governance System. This project is intentionally small, standard-library-only, and focused on governed reporting workflows.

## Local Checks

Run these before opening a pull request:

```powershell
python -m unittest discover
python -m argos_bridge validate sql_queries
python -m argos_bridge demo
```

## Report Guidelines

When adding a report:

- Add the SQL file under `sql_queries/`.
- Add matching metadata under `reports/`.
- Include report purpose, audience, parameters, and sensitivity.
- Avoid `SELECT *`.
- Use fictional sample objects only.
- Do not include credentials, production data, or personally identifiable information.

## Code Guidelines

- Keep runtime code standard-library-only.
- Prefer clear, small functions over framework-heavy patterns.
- Update tests when changing extractor, validator, or inventory behavior.
- Keep public docs project-focused and free of personal preparation notes.
