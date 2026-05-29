# 🏥 Medical Data Quality Pipeline

A production-grade ETL pipeline for medical datasets featuring extraction, cleaning, schema validation, profiling, orchestration, and observability — built with Python 3.12, containerized with Docker, and orchestrated with Dagster.

---

## 🚀 Overview

This project demonstrates a modular, production-ready ETL pipeline designed to handle messy medical data and make it analysis-ready for analytics or machine learning workflows. The architecture follows 2026 data engineering best practices: asset-centric orchestration, declarative schema validation, structured observability, and clean separation of concerns.

**Data source:** [MIMIC-IV-ED Demo](https://physionet.org/content/mimic-iv-ed/2.2/) — a publicly available emergency department dataset from PhysioNet.

---

## ⚙️ Features

- **Extract** — Pull raw medical data from multiple relational sources (MSSQL, PostgreSQL, Impala via ODBC and Thrift)
- **Transform** — Clean nulls, normalize formats, apply business rules; optional Polars fast path for large datasets
- **Validate** — Pandera schema validation at the transform stage; Great Expectations checkpoint suite at load
- **Load** — Write validated, processed data to target databases with lineage metadata
- **Orchestrate** — Dagster asset-centric pipeline with scheduling, retries, and lineage tracking
- **Observe** — Prometheus metrics + Grafana dashboards for real-time pipeline health
- **Log** — Tiered structured log outputs (info, warning, error, critical)
- **Dockerized** — Full multi-service Docker Compose environment (pipeline + Dagster webserver + Prometheus + Grafana)
- **Modular design** — Each pipeline stage is independently testable and replaceable

---

## 🏗️ Project Structure

```
PRODUCTION_ETL/
│
├── pyproject.toml              # Project metadata and dependency management (replaces requirements.txt)
├── .dockerignore
├── .env                        # Environment variables (secrets, DB credentials)
├── .env.input                  # Input environment config template
├── .gitignore
├── docker-compose.yml          # Multi-container orchestration (pipeline + Dagster + Prometheus + Grafana)
├── README.md
│
├── requirements/               # Kept for Docker layer compatibility
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
│
├── data/
│   ├── input/                  # Raw medical datasets (e.g., MIMIC-IV-ED Demo)
│   └── output/                 # Cleaned and validated output datasets
│
├── Docker/                     # Dockerfile(s) and container configs
│
├── docs/
│   ├── deployment.md
│   ├── README.md
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
├── monitoring/                 # NEW — Observability stack
│   ├── prometheus.yml          # Scrape config for pipeline metrics
│   └── grafana/
│       └── dashboards/
│           └── pipeline_health.json
│
├── notebooks/
│   └── main.ipynb
│
├── scripts/
│   ├── entrypoint.sh
│   ├── run_tests.sh
│   └── setup.sh
│
├── sql/
│   ├── queries/
│   │   └── get_active_users.sql
│   └── reporting/
│       └── faraz_daily.sql
│
├── src/
│   ├── main.py                 # Pipeline entry point (local/manual runs)
│   │
│   ├── orchestration/          # NEW — Dagster asset-centric orchestration
│   │   ├── assets.py           # Asset definitions wrapping extract/transform/load
│   │   ├── schedules.py        # Cron and event-driven scheduling
│   │   ├── resources.py        # DB connection and config resources
│   │   └── __init__.py
│   │
│   ├── config/
│   │   ├── logging_config.py
│   │   ├── settings.py
│   │   └── __init__.py
│   │
│   ├── db_connection/
│   │   ├── base.py
│   │   ├── builder.py
│   │   ├── reader.py
│   │   ├── __init__.py
│   │   └── connectors/
│   │       ├── impala_odbc.py
│   │       ├── impala_thrift.py
│   │       ├── mssql.py
│   │       ├── postgres.py
│   │       └── __init__.py
│   │
│   ├── extract/
│   │   ├── fetch_data.py
│   │   └── __init__.py
│   │
│   ├── load/
│   │   ├── load_to_db.py
│   │   └── __init__.py
│   │
│   ├── quality/                # UPGRADED — formal validation framework
│   │   ├── pandera_schemas.py  # Per-table Pandera schemas (types, ranges, nullability)
│   │   ├── gx_checkpoints.py   # Great Expectations checkpoint suite (post-load)
│   │   ├── date_validator.py   # Date/timestamp checks (refactored as Pandera custom checks)
│   │   └── __init__.py
│   │
│   ├── transform/
│   │   ├── clean_nulls.py
│   │   ├── polars_fast_path.py # NEW — Polars-based transforms for large datasets
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── metrics.py          # NEW — Prometheus instrumentation helpers
│       ├── x_parser.py
│       └── __init__.py
│
└── tests/
    ├── test_extract.py
    ├── test_load.py
    ├── test_schemas.py         # NEW — Pandera schema unit tests
    └── test_assets.py          # NEW — Dagster asset tests
```

---

## 🔧 Skills Demonstrated

- **Python 3.12** — Pandas 3.x, Polars, NumPy, modular packaging
- **ETL / ELT Design** — Asset-centric extract / transform / load architecture
- **Orchestration** — Dagster (asset definitions, schedules, sensors, lineage)
- **Data Validation** — Pandera (schema-level), Great Expectations (checkpoint-level), business-rule enforcement
- **Multi-DB Connectivity** — MSSQL, PostgreSQL, Apache Impala (ODBC + Thrift)
- **Observability** — Prometheus metrics instrumentation + Grafana dashboards
- **Docker** — Multi-service Docker Compose (pipeline, Dagster webserver, Prometheus, Grafana)
- **SQL** — Analytical and reporting queries on medical datasets
- **Testing** — Unit tests for extract, load, schemas, and Dagster assets
- **Logging** — Structured multi-level logging for production observability
- **Documentation** — Schema dictionaries, ER diagrams, pipeline flow docs

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.12+
- Access credentials configured in `.env`

### Run with Docker (recommended)

Starts the full stack: pipeline, Dagster UI, Prometheus, and Grafana.

```bash
docker-compose up --build
```

| Service          | URL                        |
|------------------|----------------------------|
| Dagster UI       | http://localhost:3000       |
| Grafana          | http://localhost:3001       |
| Prometheus       | http://localhost:9090       |

### Run locally

```bash
# Install dependencies
pip install -e ".[dev]"

# Set up environment
cp .env.input .env
# Edit .env with your DB credentials

# Run the pipeline manually
python src/main.py

# Or launch the Dagster dev server
dagster dev -f src/orchestration/assets.py
```

### Run tests

```bash
bash scripts/run_tests.sh

# Or directly
pytest tests/ -v
```

---

## ✅ Data Validation Architecture

Validation runs at two stages:

**Stage 1 — Transform (Pandera)**
Schema-level checks applied immediately after cleaning: column types, value ranges, null constraints, and custom date checks. Failures halt the pipeline before bad data reaches the database.

```python
# Example: src/quality/pandera_schemas.py
import pandera as pa

EdVisitSchema = pa.DataFrameSchema({
    "subject_id":   pa.Column(int, nullable=False),
    "intime":       pa.Column("datetime64[ns]", nullable=False),
    "outtime":      pa.Column("datetime64[ns]", nullable=True),
    "temperature":  pa.Column(float, pa.Check.in_range(30.0, 45.0), nullable=True),
    "heartrate":    pa.Column(float, pa.Check.in_range(0, 300), nullable=True),
})
```

**Stage 2 — Post-load (Great Expectations)**
Checkpoint suite runs against the loaded data: row counts, referential integrity, freshness checks, and anomaly detection. Results are stored and surfaced in the Dagster UI.

---

## 📊 Observability

Pipeline metrics are exposed via Prometheus and visualized in Grafana:

| Metric | Description |
|--------|-------------|
| `etl_records_extracted_total` | Total records pulled per source |
| `etl_records_failed_validation_total` | Validation failures by table and check |
| `etl_pipeline_duration_seconds` | End-to-end runtime per pipeline run |
| `etl_records_loaded_total` | Records successfully written to target |

---

## 🗂️ Dependency Management

This project uses `pyproject.toml` as the canonical dependency spec.

```toml
[project]
name = "medical-etl-pipeline"
requires-python = ">=3.12"

dependencies = [
    "pandas>=3.0",
    "polars>=1.0",
    "pandera>=0.20",
    "great-expectations>=1.2",
    "dagster>=1.8",
    "dagster-webserver",
    "sqlalchemy>=2.0",
    "prometheus-client>=0.20",
    "openlineage-python>=1.18",
]

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]
```

The `requirements/` folder is kept for Docker layer caching compatibility.

---

## 📌 Status

🚧 **In active development** — core pipeline stages (extract, transform, load, quality) are implemented. Dagster orchestration and Grafana dashboards in progress.

---

## 📚 References

- [MIMIC-IV-ED Demo Dataset — PhysioNet](https://physionet.org/content/mimic-iv-ed/2.2/)
- [Dagster Documentation](https://docs.dagster.io)
- [Pandera Documentation](https://pandera.readthedocs.io)
- [Great Expectations Documentation](https://docs.greatexpectations.io)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
