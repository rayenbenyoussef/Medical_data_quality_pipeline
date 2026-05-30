# 🏥 Medical Data Quality Pipeline

A production-grade ELT pipeline for medical datasets — built on the tools that 57,000+ companies actually run in production: Python, Apache Airflow, dbt, PostgreSQL, Docker, Pandas, Pandera, Prometheus, and Grafana.

---

## 🚀 Overview

This project demonstrates a modular, production-ready ELT pipeline designed to handle messy medical data and make it analysis-ready for analytics or machine learning workflows.

The stack is built entirely on tools that dominate real job postings and company infrastructure in 2026 — no niche frameworks, no early-stage bets. Every tool here is battle-tested, widely documented, and actively hiring for.

**Data source:** [MIMIC-IV-ED Demo](https://physionet.org/content/mimic-iv-ed/2.2/) — a publicly available emergency department dataset from PhysioNet.

---

## 🧱 The Stack — Why Each Tool

| Tool | Role | Why It's Here |
|------|------|---------------|
| **Python 3.12** | Core language | In 78%+ of all DE job postings |
| **Apache Airflow 3** | Orchestration | 8,375+ companies, OpenAI runs 7,000 pipelines on it |
| **dbt Core** | Transformation | 57,000+ companies, the SQL transformation standard |
| **PostgreSQL** | Source + target DB | Most widely used open-source relational DB |
| **Pandas 3.x** | In-memory processing | 77% adoption among data engineers |
| **Pandera** | DataFrame validation | Production-ready schema testing for Pandas/Polars |
| **Docker + Compose** | Containerization | 59% of professional developers, fully reproducible |
| **Prometheus + Grafana** | Observability | Industry standard monitoring stack |
| **SQLAlchemy 2.x** | DB connectivity | Standard Python DB abstraction layer |
| **pytest** | Testing | Standard Python testing framework |

---

## ⚙️ Features

- **Extract** — Pull raw medical data from PostgreSQL and MSSQL via SQLAlchemy connection factory
- **Load (raw)** — Land raw records into a PostgreSQL staging schema without transformation
- **Transform (dbt)** — Clean, normalize, and apply business rules using version-controlled SQL dbt models with tests
- **Validate** — Pandera schema checks on all DataFrames before loading; dbt tests on all models after
- **Orchestrate** — Apache Airflow DAGs with scheduling, retries, and dependency management
- **Observe** — Prometheus metrics exposed per pipeline run; Grafana dashboard for health visualization
- **Log** — Structured multi-level logging (info / warning / error / critical) to tiered log files
- **Containerized** — Full stack runs with a single `docker-compose up` command

---

## 🏗️ Project Structure

```
PRODUCTION_ETL/
│
├── pyproject.toml              # Project metadata and dependencies (modern standard)
├── .dockerignore
├── .env                        # Secrets and DB credentials (never committed)
├── .env.input                  # Template for environment config
├── .gitignore
├── docker-compose.yml          # Full stack: pipeline + Airflow + PostgreSQL + Prometheus + Grafana
├── README.md
│
├── requirements/               # Kept for Docker layer caching compatibility
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── data/
│   ├── input/                  # Raw MIMIC-IV-ED source files
│   └── output/                 # Processed and validated output datasets
│
├── dbt/                        # dbt project — all SQL transformations live here
│   ├── dbt_project.yml         # dbt project config
│   ├── profiles.yml            # DB connection profiles
│   ├── models/
│   │   ├── staging/            # Raw → typed, renamed, light cleaning
│   │   │   ├── stg_edstays.sql
│   │   │   ├── stg_triage.sql
│   │   │   └── stg_vitalsign.sql
│   │   └── marts/              # Business-logic models, ready for analytics
│   │       ├── fct_ed_visits.sql
│   │       └── dim_patients.sql
│   ├── tests/                  # dbt data tests (not-null, unique, range checks)
│   │   └── assert_vitals_in_range.sql
│   └── macros/                 # Reusable Jinja SQL macros
│
├── dags/                       # Airflow DAG definitions
│   ├── medical_etl_dag.py      # Main ELT pipeline DAG (daily schedule)
│   └── data_quality_dag.py     # Standalone validation DAG
│
├── Docker/                     # Dockerfile(s) for pipeline and Airflow images
│
├── docs/
│   ├── deployment.md
│   ├── etl/
│   │   ├── business_rules.md
│   │   └── pipeline_flow.md
│   └── schema/
│       ├── data_dictionary.csv
│       └── er_diagram.md
│
├── logs/
│   ├── critical.log
│   ├── error.log
│   ├── info.log
│   └── warning.log
│
├── monitoring/
│   ├── prometheus.yml          # Scrape config for pipeline and Airflow metrics
│   └── grafana/
│       └── dashboards/
│           └── pipeline_health.json
│
├── notebooks/
│   └── main.ipynb              # Exploratory analysis and profiling
│
├── scripts/
│   ├── entrypoint.sh
│   ├── run_tests.sh
│   └── setup.sh
│
├── sql/
│   ├── queries/
│   │   └── get_active_patients.sql
│   └── reporting/
│       └── daily_summary.sql
│
├── src/
│   ├── main.py                 # Manual pipeline entry point (local runs)
│   │
│   ├── config/
│   │   ├── logging_config.py   # Structured logging setup
│   │   ├── settings.py         # Environment parsing and global config
│   │   └── __init__.py
│   │
│   ├── db_connection/          # DB abstraction layer
│   │   ├── base.py             # Abstract connection interface
│   │   ├── builder.py          # Connection factory (SQLAlchemy engines)
│   │   ├── reader.py           # Generic query execution
│   │   ├── __init__.py
│   │   └── connectors/
│   │       ├── mssql.py
│   │       ├── postgres.py
│   │       └── __init__.py
│   │
│   ├── extract/
│   │   ├── fetch_data.py       # Pull raw data from source DBs into DataFrames
│   │   └── __init__.py
│   │
│   ├── load/
│   │   ├── load_to_staging.py  # Write raw data to PostgreSQL staging schema
│   │   └── __init__.py
│   │
│   ├── quality/
│   │   ├── pandera_schemas.py  # Per-table Pandera schemas (types, ranges, nulls)
│   │   ├── date_validator.py   # Medical timestamp checks as Pandera custom checks
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── metrics.py          # Prometheus counter/gauge helpers
│       ├── x_parser.py         # XML/custom format parser
│       └── __init__.py
│
└── tests/
    ├── test_extract.py
    ├── test_load.py
    ├── test_schemas.py         # Pandera schema unit tests
    └── test_dbt_models.py      # dbt model output validation tests
```

---

## 🔄 Pipeline Architecture

```
[Source DBs: PostgreSQL / MSSQL]
        │
        ▼  (SQLAlchemy)
[Extract: fetch_data.py]         ← Pandera validation at this layer
        │
        ▼
[Load to Staging: PostgreSQL]    ← Raw schema, no transformation
        │
        ▼  (dbt run)
[Transform: dbt models]          ← staging/ → marts/ with dbt tests
        │
        ▼
[Marts: PostgreSQL]              ← Analytics-ready tables
        │
        ▼
[Airflow DAG orchestrates all above with scheduling + retries]
        │
        ▼
[Prometheus metrics → Grafana dashboard]
```

---

## 🔧 Skills Demonstrated

This project was built as a hands-on learning portfolio. Skills are split between what I applied from prior experience and what I learned specifically to build this project.

### Applied from prior experience
- **Python 3.12** — OOP, abstract base classes, type hints, modular packaging with `pyproject.toml`
- **SQL & PostgreSQL** — Window functions, CTEs, schema design (staging vs marts pattern), DDL
- **Pandas 3.x** — Data cleaning, datetime normalization, Parquet I/O, memory-efficient reads

### Learned to build this project
- **SQLAlchemy 2.x** — Abstract connection factory, multi-DB support (PostgreSQL + MSSQL), connection pooling
- **dbt Core** — Staging/marts model design, YAML schema tests, Jinja macros, auto-generated lineage docs
- **Apache Airflow 3** — DAG authoring, PythonOperator, BashOperator, cron scheduling, retries, Connections
- **Pandera** — Per-table DataFrame schemas, medical-domain range checks, custom validators
- **Docker & Compose** — Multi-service stack (pipeline + Airflow + PostgreSQL + Prometheus + Grafana), volumes, networking
- **pytest** — Fixtures, mocking DB connections, Pandera schema tests, coverage reporting, GitHub Actions CI
- **Prometheus + Grafana** — Pipeline metrics instrumentation, scrape config, dashboard building
- **Logging** — Structured tiered logging (info / warning / error / critical) for production observability
- **Medical domain** — MIMIC-IV-ED schema, clinical data ranges, PHI concepts, data dictionary authoring

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.12+
- Credentials configured in `.env`

### Run the full stack with Docker

```bash
docker-compose up --build
```

| Service | URL |
|---------|-----|
| Airflow UI | http://localhost:8080 |
| Grafana | http://localhost:3001 |
| Prometheus | http://localhost:9090 |

### Run locally

```bash
# Install dependencies
pip install -e ".[dev]"

# Configure environment
cp .env.input .env

# Run extract + load to staging
python src/main.py

# Run dbt transformations
cd dbt && dbt run && dbt test

# Trigger the Airflow DAG manually
airflow dags trigger medical_etl_dag
```

### Run tests

```bash
bash scripts/run_tests.sh
# or
pytest tests/ -v --cov=src
```

---

## ✅ Data Validation — Two Layers

### Layer 1 — Python (Pandera)
Runs in `src/quality/pandera_schemas.py` immediately after extraction. Catches bad types, null violations, and out-of-range medical values before anything reaches the database.

```python
import pandera as pa

EdStaysSchema = pa.DataFrameSchema({
    "subject_id":  pa.Column(int, nullable=False),
    "intime":      pa.Column("datetime64[ns]", nullable=False),
    "outtime":     pa.Column("datetime64[ns]", nullable=True),
    "temperature": pa.Column(float, pa.Check.in_range(30.0, 45.0), nullable=True),
    "heartrate":   pa.Column(float, pa.Check.in_range(0, 300),     nullable=True),
})
```

### Layer 2 — SQL (dbt tests)
Runs after `dbt run`. Tests are declared in YAML and executed as SQL assertions against the warehouse.

```yaml
# dbt/models/staging/schema.yml
models:
  - name: stg_edstays
    columns:
      - name: subject_id
        tests: [not_null, unique]
      - name: intime
        tests: [not_null]
```

---

## 📊 Observability

| Metric | Description |
|--------|-------------|
| `etl_records_extracted_total` | Records pulled per source table |
| `etl_records_failed_validation_total` | Pandera failures by table and check name |
| `etl_pipeline_duration_seconds` | End-to-end run time per DAG execution |
| `etl_records_loaded_total` | Records successfully written to staging |
| `dbt_models_passed_total` | dbt models that completed successfully |
| `dbt_tests_failed_total` | dbt test failures by model |

---

## 📦 Dependencies (`pyproject.toml`)

```toml
[project]
name = "medical-etl-pipeline"
requires-python = ">=3.12"

dependencies = [
    # Core
    "pandas>=3.0",
    "numpy>=1.26",
    "sqlalchemy>=2.0",
    # Orchestration
    "apache-airflow>=3.0",
    # Validation
    "pandera>=0.20",
    # Observability
    "prometheus-client>=0.20",
    # DB drivers
    "psycopg2-binary>=2.9",
    "pyodbc>=5.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov", "ruff", "mypy", "dbt-core>=1.8", "dbt-postgres>=1.8"]
```

---

## 📊 Data Sources

Built against the **[MIMIC-IV-ED Demo](https://physionet.org/content/mimic-iv-ed/2.2/)** — a publicly available emergency department dataset from PhysioNet covering tables: `edstays`, `triage`, `vitalsign`, `medrecon`, `pyxis`.

---

## 📌 Status

🚧 **In active development** — extract, load, Pandera validation, and dbt staging models complete. Airflow DAGs and Grafana dashboards in progress.

---

## 🎯 Why This Stack

Every tool in this project was chosen based on verified production adoption data, not trends:

| Tool | Adoption Evidence |
|------|-------------------|
| Apache Airflow | 8,375+ companies · OpenAI runs 7,000 pipelines on it |
| dbt Core | 57,000+ companies · de facto SQL transformation standard |
| PostgreSQL | Most widely used open-source relational database |
| Docker | 59% of professional developers use it daily |
| Pandas | 77% adoption among data engineers |
| Prometheus + Grafana | Industry-standard open-source monitoring stack |

No experimental frameworks. No early-stage bets. Everything here is in active production at companies that are hiring.
