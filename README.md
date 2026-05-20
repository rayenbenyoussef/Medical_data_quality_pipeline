# 🏥 Medical Data Quality Pipeline

A production-grade ETL pipeline showcasing experience with medical datasets — including extraction, cleaning, validation, profiling, and loading — built with Python and containerized with Docker.

---

## 🚀 Overview

This project demonstrates a modular, production-ready ETL pipeline designed to handle messy medical data and make it analysis-ready for analytics or machine learning workflows. The architecture emphasizes clean separation of concerns, robust logging, multi-database connectivity, and scalable design patterns.

---

## ⚙️ Features

- **Extract**: Pull raw medical data from multiple relational database sources (MSSQL, PostgreSQL, Impala via ODBC and Thrift).
- **Transform**: Clean nulls, normalize formats, and apply business rules to raw records.
- **Load**: Write validated, processed data back to target databases.
- **Quality checks**: Date validation and configurable data quality rules.
- **Logging**: Tiered log outputs (info, warning, error, critical) for full pipeline observability.
- **Dockerized**: Fully containerized environment with Docker Compose for reproducible deployments.
- **Modular design**: Each pipeline stage is independently testable and replaceable.

---

## 🏗️ Project Structure

```
PRODUCTION_ETL/
│
├── .dockerignore
├── .env                        # Environment variables (secrets, DB credentials)
├── .env.input                  # Input environment config template
├── .gitignore
├── docker-compose.yml          # Multi-container orchestration
├── README.md
├── requirements.txt
│
├── data/
│   ├── input/                  # Raw medical datasets (e.g., MIMIC-IV-ED Demo)
│   └── output/                 # Cleaned and validated output datasets
│
├── Docker/                     # Dockerfile(s) and container configs
│
├── docs/
│   ├── deployment.md           # Deployment instructions
│   ├── README.md               # Docs overview
│   ├── etl/
│   │   ├── business_rules.md   # Data transformation and validation rules
│   │   └── pipeline_flow.md    # End-to-end pipeline architecture diagram
│   └── schema/
│       ├── data_dictionary.csv # Field definitions and medical terminology
│       └── er_diagram.md       # Entity-relationship diagram
│
├── logs/
│   ├── critical.log
│   ├── error.log
│   ├── info.log
│   └── warning.log
│
├── notebooks/
│   └── main.ipynb              # Exploratory analysis and pipeline demos
│
├── requirements/
│   ├── base.txt                # Shared dependencies
│   ├── dev.txt                 # Development extras (testing, linting)
│   └── prod.txt                # Production-only dependencies
│
├── scripts/
│   ├── entrypoint.sh           # Docker container entrypoint
│   ├── run_tests.sh            # Test runner script
│   └── setup.sh                # Environment setup script
│
├── sql/
│   ├── queries/
│   │   └── get_active_users.sql
│   └── reporting/
│       └── faraz_daily.sql
│
├── src/
│   ├── main.py                 # Pipeline entry point
│   │
│   ├── config/
│   │   ├── logging_config.py   # Logging setup and handlers
│   │   ├── settings.py         # Global settings and environment parsing
│   │   └── __init__.py
│   │
│   ├── db_connection/
│   │   ├── base.py             # Abstract DB connection interface
│   │   ├── builder.py          # Connection factory/builder
│   │   ├── reader.py           # Generic query execution
│   │   ├── __init__.py
│   │   └── connectors/
│   │       ├── impala_odbc.py
│   │       ├── impala_thrift.py
│   │       ├── mssql.py
│   │       ├── postgres.py
│   │       └── __init__.py
│   │
│   ├── extract/
│   │   ├── fetch_data.py       # Data extraction logic
│   │   └── __init__.py
│   │
│   ├── load/
│   │   ├── load_to_db.py       # Writes processed data to target DB
│   │   └── __init__.py
│   │
│   ├── quality/
│   │   ├── date_validator.py   # Medical timestamp and date range checks
│   │   └── __init__.py
│   │
│   ├── transform/
│   │   ├── clean_nulls.py      # Null handling and imputation strategies
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── x_parser.py         # XML/custom format parser
│       └── __init__.py
│
└── tests/
    ├── test_extract.py
    └── test_load.py
```

---

## 🔧 Skills Demonstrated

- **Python** — Pandas, NumPy, modular packaging with `__init__.py`
- **ETL Design** — Layered extract / transform / load architecture
- **Multi-DB Connectivity** — MSSQL, PostgreSQL, Apache Impala (ODBC + Thrift)
- **Data Quality** — Null handling, date validation, business-rule enforcement
- **Docker** — Containerized pipeline via Docker Compose
- **SQL** — Analytical and reporting queries on medical datasets
- **Testing** — Unit tests for extract and load stages
- **Logging** — Structured multi-level logging for production observability
- **Documentation** — Schema dictionaries, ER diagrams, pipeline flow docs

---

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- Access credentials configured in `.env`

### Run with Docker

```bash
docker-compose up --build
```

### Run locally

```bash
# Install dependencies
pip install -r requirements/dev.txt

# Set up environment
cp .env.input .env
# Edit .env with your DB credentials

# Run the pipeline
python src/main.py
```

### Run tests

```bash
bash scripts/run_tests.sh
```

---

## 📊 Data Sources

This pipeline is designed to work with real-world hospital datasets. For development and demonstration, it targets the **[MIMIC-IV-ED Demo](https://physionet.org/content/mimic-iv-ed/2.2/)** dataset — a publicly available emergency department dataset from PhysioNet.

---

## 📌 Status

🚧 **In active development** — core pipeline stages (extract, transform, load, quality) are implemented. Reporting and extended quality modules in progress.
