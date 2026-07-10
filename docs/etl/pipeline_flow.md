# Pipeline Flow

## Overview
Raw CSV files → PostgreSQL raw layer → dbt staging → dbt marts → validation → downstream

## Steps
1. **Extract** — 6 CSV files from MIMIC-IV-ED dataset (data/input/)
2. **Load Raw** — CSVRawLoader loads each CSV into raw schema (PostgreSQL)
3. **Validate Raw** — RawLoadValidator checks row counts, column counts, nulls
4. **dbt Staging** — clean, rename, cast types, handle NULLs
5. **dbt Marts** — dimensional model (star schema)
6. **dbt Tests** — data tests across all models
7. **Extract Mart** — MartExtractor reads mart tables into DataFrames
8. **Validate Mart** — Pandera schemas validate DataFrame structure/types
9. **Orchestration** — Airflow DAGs automate steps 1-8 on schedule

## Data Flow Diagram
CSV → [CSVLoader] → raw.* → [dbt staging] → stg.* → [dbt marts] → mrt.*