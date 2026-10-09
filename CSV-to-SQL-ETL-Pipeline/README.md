# CSV-to-SQL ETL Pipeline | Python + Pandas + SQLite

A beginner-friendly, reproducible **data engineering portfolio project**. Extract retail transactions from CSV, validate and transform records with Pandas, and load clean data into a SQLite database for SQL reporting.

## Pipeline

`CSV -> Pandas validation & deduplication -> SQLite (upsert) -> SQL reporting`

## Features
- Required-column validation and date/number parsing
- Rejection of missing, nonpositive quantities, negative prices and duplicate order IDs
- Derived `line_total` calculation
- Idempotent SQLite loading using primary-key upserts
- Separate rejected-rows export
- Four example SQL analytics queries
- Automated tests and GitHub Actions workflow

## Run locally (Windows / macOS / Linux)

Requires Python 3.10+. Run from this project folder:

```bash
python -m pip install -r requirements.txt
python -m src.etl --input data/sample_sales.csv --db data/sales.db
python -m pytest -q
```

Open `data/sales.db` with a SQLite viewer or Python's built-in `sqlite3` and execute `sql/analytics.sql`.

## Data provenance
`data/sample_sales.csv` is **synthetic demonstration data**, authored solely to exercise the pipeline. It is not real customer or company data. Five unique valid orders and two intentionally invalid/duplicate records are included. The project does not claim production deployment or business impact.

## Future enhancements
- Row-level rejection reasons and structured logging
- Incremental processing and file-level audit trail
- Configuration-driven schema validation
- PostgreSQL support and scheduled runs
- Data quality dashboard

## Resume bullet (only after you've run and understood the project)
Built a Python/Pandas ETL pipeline to validate and deduplicate retail CSV transactions, load clean records into SQLite with idempotent upserts, and generate SQL-based revenue reports.
