# Deployment Guide

## Overview

Medical Data Quality Pipeline is a data engineering project built on top of the
MIMIC-IV-ED dataset. It extracts raw clinical data from CSV files, loads it into
PostgreSQL, transforms it using dbt into a star schema dimensional model, and
validates data quality at every layer.

---

## Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.14+ | Core pipeline language |
| PostgreSQL | 14+ | Data warehouse |
| dbt-postgres | 1.10+ | SQL transformations |
| Git | any | Version control |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/rayenbenyoussef/Medical_data_quality_pipeline
cd Medical_data_quality_pipeline
```

### 2. Create and activate virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements/base.txt
```

### 4. Configure environment variables

```bash
cp .env.input .env
# open .env and fill in your credentials
```

Required variables:

| Variable | Description | Example |
|---|---|---|
| DB_TYPE | Database type | postgres |
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_NAME | Database name | medical_test |
| DB_USER | Database username | rayen |
| DB_PASSWORD | Database password | **** |
| RAW_SCHEMA | Raw layer schema name | raw |
| STG_SCHEMA | Staging layer schema name | stg |
| MRT_SCHEMA | Mart layer schema name | mrt |

### 5. Create PostgreSQL schemas

Connect to your PostgreSQL instance and run:

```sql
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS stg;
CREATE SCHEMA IF NOT EXISTS mrt;
```

### 6. Install dbt packages

```bash
cd dbt
dbt deps
cd ..
```

### 7. Verify dbt connection

```bash
cd dbt
dbt debug
cd ..
```

---

## Running the Pipeline

### Full pipeline (recommended)

Runs all steps in order: load raw → validate → dbt run → dbt test → extract → validate mart

```bash
python src/main.py
```

### Individual steps

**Load CSV files to raw layer only:**
```bash
python -c "
from config.Config import DbConfig
from db_connection.builder import ConnectionBuilder
from load.load_to_raw import CSVRawLoader
from db_connection.writer import DBWriter

config = DbConfig.get_config()
db = ConnectionBuilder().build(config)
loader = CSVRawLoader(DBWriter(db), config['raw'])
"
```

**Run dbt transformations:**
```bash
cd dbt
dbt run
```

**Run dbt tests:**
```bash
cd dbt
dbt test
```

**Run dbt for specific layer:**
```bash
cd dbt
dbt run --select path:models/staging    # staging only
dbt run --select path:models/marts      # marts only
```

---

## Running Tests

### Python unit tests (no database needed)

```bash
pytest tests/ -v -m "not integration"
```

### Python integration tests (requires database)

```bash
pytest tests/ -v -m integration
```

### All tests

```bash
pytest tests/ -v
```

### dbt tests only

```bash
cd dbt
dbt test
```

---

## Project Structure

```
medical-data-quality-pipeline/
│
├── data/
│   └── input/              # Source CSV files (MIMIC-IV-ED dataset)
│       ├── edstays.csv
│       ├── triage.csv
│       ├── vitalsign.csv
│       ├── diagnosis.csv
│       ├── medrecon.csv
│       └── pyxis.csv
│
├── dbt/
│   ├── models/
│   │   ├── staging/        # Raw → cleaned (one model per source table)
│   │   └── marts/          # Star schema dimensional model
│   ├── macros/             # Reusable SQL macros (pain_filter, fahr_to_celsius...)
│   ├── seeds/              # Static reference data (discharge status codes)
│   └── tests/              # Custom dbt singular tests
│
├── src/
│   ├── config/             # Environment configuration
│   ├── db_connection/      # Database abstraction layer (Postgres + MSSQL)
│   ├── load/               # CSV → raw schema loader
│   ├── extract/            # Mart data extractor
│   ├── quality/            # Data validation (raw + mart layers)
│   └── main.py             # Pipeline entry point
│
├── tests/                  # Python unit + integration tests
├── docs/                   # Project documentation
├── requirements/           # Python dependencies
│   ├── base.txt            # Core dependencies
│   ├── dev.txt             # Development + testing dependencies
│   └── prod.txt            # Production dependencies
└── .env.input              # Environment variable template
```

---

## Data Flow

```
CSV files (MIMIC-IV-ED)
    ↓
[CSVRawLoader] — pandas reads CSV, inserts to PostgreSQL with transaction safety
    ↓
raw.* (PostgreSQL) — untouched source data
    ↓
[RawLoadValidator] — checks row counts, column counts, required nulls
    ↓
[dbt staging] — casts types, renames columns, handles NULLs, standardizes values
    ↓
stg.* (PostgreSQL) — clean, typed, standardized data
    ↓
[dbt marts] — builds star schema (dimensions + facts + bridge tables)
    ↓
mrt.* (PostgreSQL) — analytics-ready dimensional model
    ↓
[dbt test] — 166 data quality tests across all models
    ↓
[MartExtractor] — reads mart tables into pandas DataFrames
    ↓
[MartValidator] — Pandera schema validation on extracted DataFrames
```

---

## Database Schema

### Raw Layer (`raw.*`)
One table per source CSV file, loaded as-is with minimal transformation:
- `raw.edstays`, `raw.triage`, `raw.vitalsign`
- `raw.diagnosis`, `raw.medrecon`, `raw.pyxis`

### Staging Layer (`stg.*`)
One model per source table, cleaned and typed:
- `stg.stg_edstays`, `stg.stg_triage`, `stg.stg_vitalsign`
- `stg.stg_diagnosis`, `stg.stg_medrecon`, `stg.stg_pyxis`

### Mart Layer (`mrt.*`)
Star schema dimensional model:

**Dimensions:**
- `mrt.dim_patients` — patient demographics
- `mrt.dim_date` — calendar date dimension
- `mrt.dim_hour` — time-of-day dimension (minute granularity)
- `mrt.dim_medications` — medication reference
- `mrt.dim_icd_classification` — ICD diagnosis codes
- `mrt.dim_etc_classification` — therapeutic classification codes
- `mrt.dim_chiefcomplaint` — chief complaint categories

**Facts:**
- `mrt.fct_ed_visits` — one row per ED visit (central fact table, includes triage)
- `mrt.fct_vitalsigns` — repeated vital sign measurements per visit
- `mrt.fct_diagnosis` — diagnoses per visit
- `mrt.fct_medrecon` — pre-visit medications per patient
- `mrt.fct_pyxis` — medications dispensed during visit

**Bridge:**
- `mrt.bridge_triage_complaints` — visit ↔ chief complaint (many-to-many)

---

## Planned Enhancements

The following features are planned but not yet implemented:

- **Docker containerization** — `docker-compose.yml` scaffolding exists
- **Airflow orchestration** — DAG files exist as stubs (`dags/`)
- **Grafana monitoring dashboards** — dashboard JSON scaffolding exists
- **Prometheus metrics** — `monitoring/prometheus.yml` scaffolding exists
- **MSSQL support** — Python connectors built, dbt models are Postgres-only

---

## Dataset

This project uses the **MIMIC-IV-ED** dataset (Medical Information Mart for
Intensive Care — Emergency Department), a real de-identified clinical dataset
from Beth Israel Deaconess Medical Center, Boston.

Access requires credentialing via PhysioNet:
https://physionet.org/content/mimic-iv-ed/

---

## Author

Rayen Ben Youssef
GitHub: https://github.com/rayenbenyoussef