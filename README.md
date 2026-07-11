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
medical_data_quality_pipeline/
│
├── pyproject.toml              # Project metadata and dependencies (modern standard)
├── .dockerignore
├── .env                        # Secrets and DB credentials (never committed)
├── .env.input                  # Template for environment config
├── .gitignore
├── docker-compose.yml          # Full stack: pipeline + Airflow + PostgreSQL + Prometheus + Grafana
├── pytest.ini 
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
│   │   │   ├── stg_models.yml
│   │   │   ├── sources.yml
│   │   │   ├── stg_triage.sql
│   │   │   ├── stg_diagnosis.sql
│   │   │   ├── stg_medrecon.sql
│   │   │   ├── stg_edstays.sql
│   │   │   ├── stg_pyxis.sql
│   │   │   └── stg_vitalsign.sql
│   │   └── marts/              # Business-logic models, ready for analytics
│   │       ├── fct_ed_visits.sql
│   │       ├── fct_vitalsigns.sql
│   │       ├── fct_pyxis.sql
│   │       ├── fct_medrecon.sql
│   │       ├── fct_diagnosis.sql
│   │       ├── dim_medications.sql
│   │       ├── dim_icd_classification.sql
│   │       ├── dim_hour.sql
│   │       ├── dim_etc_classification.sql
│   │       ├── dim_date.sql
│   │       ├── dim_chiefcomplaint.sql
│   │       ├── dim_patients.sql
│   │       └── bridge_triage_complaints.sql
│   │       
│   ├── tests/                  # dbt data tests (not-null, unique, range checks)
│   │   └── test_dim_patients_contains_ed_patients.sql
│   └── macros/                 # Reusable Jinja SQL macros
│       ├── between_nulling.sql
│       ├── extract_country.sql
│       ├── extract_race.sql
│       ├── fahr_to_celsius.sql
│       └── pain_filter.sql
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
│       ├── mart_diagram.pdf
│       └── staging_diagram.pdf
│
├── logs/
│   ├── debug.log
│   ├── errors.log
│   └── pipeline.log
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
│   │   ├── Config.py         # Environment parsing and global config
│   │   └── __init__.py
│   │
│   ├── db_connection/          # DB abstraction layer
│   │   ├── base.py             # Abstract connection interface
│   │   ├── builder.py          # Connection factory (SQLAlchemy engines)
│   │   ├── reader.py           # Generic query execution
│   │   ├── writer.py 
│   │   ├── __init__.py
│   │   └── connectors/
│   │       ├── exceptions.py
│   │       ├── mssql.py
│   │       ├── postgres.py
│   │       └── __init__.py
│   │
│   ├── extract/
│   │   ├── fetch_data.py       # Pull raw data from source DBs into DataFrames
│   │   └── __init__.py
│   │
│   ├── load/
│   │   ├── load_to_raw.py  # Write raw data to PostgreSQL staging schema
│   │   └── __init__.py
│   │
│   ├── quality/
│   │   ├── raw_validator.py
│   │   ├── mart_validator.py
│   │   ├── pandera_schemas.py  # Per-table Pandera schemas (types, ranges, nulls)
│   │   ├── date_validator.py   # Medical timestamp checks as Pandera custom checks
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── metrics.py          # Prometheus counter/gauge helpers
│       ├── x_parser.py         # XML/custom format parser
│       ├── sql_helpers.py   
│       └── __init__.py
│
└── tests/
    ├── conftest.py
    ├── test_extract.py
    ├── test_load.py
    ├── test_schemas.py         # Pandera schema unit tests
    └── test_dbt_models.py      # dbt model output validation tests
```

---

## 🔧 Skills Demonstrated

This project was built as a hands-on learning portfolio. Skills are split between what I applied from prior experience and what I learned specifically to build this project.

### Applied from prior experience
- **Python 3.12** — OOP, abstract base classes, type hints, modular packaging with `pyproject.toml`
- **SQL & PostgreSQL** — Window functions, CTEs, schema design (staging vs marts pattern), DDL
- **Pandas 3.x** — Data cleaning, datetime normalization, Parquet I/O, memory-efficient reads

### Learned to build this project
- **dbt Core** — Staging/marts model design, YAML schema tests, Jinja macros, auto-generated lineage docs
- **Apache Airflow 3** — DAG authoring, PythonOperator, BashOperator, cron scheduling, retries, Connections
- **Pandera** — Per-table DataFrame schemas, medical-domain range checks, custom validators
- **Docker & Compose** — Multi-service stack (pipeline + Airflow + PostgreSQL + Prometheus + Grafana), volumes, networking
- **pytest** — Fixtures, mocking DB connections, Pandera schema tests, coverage reporting, GitHub Actions CI
- **Prometheus + Grafana** — Pipeline metrics instrumentation, scrape config, dashboard building
- **Logging** — Structured tiered logging (info / warning / error / critical) for production observability
- **Medical domain** — MIMIC-IV-ED schema, clinical data ranges, PHI concepts, data dictionary authoring

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

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.12+
- PostgresSql
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

See the installation guide: [Installation](docs/deployment.md)

---

## 📊 Data Sources

Built against the **[MIMIC-IV-ED Demo](https://physionet.org/content/mimic-iv-ed/2.2/)** — a publicly available emergency department dataset from PhysioNet covering tables: `edstays`, `triage`, `vitalsign`, `medrecon`, `pyxis`.

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

## Author

Rayen Ben Youssef
GitHub: https://github.com/rayenbenyoussef