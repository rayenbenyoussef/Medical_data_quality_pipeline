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
| Python | 3.12+ | Core pipeline language |
| PostgreSQL | 14+ | Data warehouse |
| dbt-postgres | 1.10+ | SQL transformations |
| Docker | any | Container runtime (for Docker setup) |
| Git | any | Version control |

---

## Option 1 — Docker Setup (Recommended)

Runs the full stack (Airflow + PostgreSQL + Grafana) with one command.

### 1. Clone the repository

```bash
git clone https://github.com/rayenbenyoussef/Medical_data_quality_pipeline
cd Medical_data_quality_pipeline
```

### 2. Configure environment variables

**Windows (Command Prompt):**
```cmd
copy .env.input .env
```

**Windows (PowerShell):**
```powershell
Copy-Item .env.input .env
```

**Linux/Mac:**
```bash
cp .env.input .env
```

Fill in your credentials in `.env`:

| Variable | Description | Example |
|---|---|---|
| DB_TYPE | Database type | postgres |
| DB_HOST | Database host | postgres |
| DB_PORT | Database port | 5432 |
| DB_NAME | Database name | medical |
| DB_USER | Database username | airflow |
| DB_PASSWORD | Database password | **** |
| RAW_SCHEMA | Raw layer schema name | raw |
| STG_SCHEMA | Staging layer schema name | stg |
| MRT_SCHEMA | Mart layer schema name | mrt |
| PROJECT_ROOT | Absolute path to project | /opt/airflow |
| AIRFLOW_PROJ_DIR | Project directory for Docker | . |
| FERNET_KEY | Airflow encryption key | (generate one) |

### 3. Generate Fernet key (required for Airflow)

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Add the output to `.env` as `FERNET_KEY=...`

### 4. Start the full stack

```bash
docker-compose up --build
```

Wait ~2 minutes for all services to initialize.

### 5. Access services

| Service | URL | Default credentials |
|---|---|---|
| Airflow UI | http://localhost:8080 | airflow / airflow |
| Grafana | http://localhost:3000 | admin / admin |

### 6. Trigger the pipeline

1. Go to Airflow UI → **DAGs**
2. Enable `medical_etl_init`
3. Click **Trigger DAG** to run the full pipeline
4. Monitor progress in the DAG graph view

### Stop the stack

```bash
docker-compose down
```

### Stop and remove all data

```bash
docker-compose down -v
```

---

## Option 2 — Local Setup (Manual)

### 1. Clone the repository

```bash
git clone https://github.com/rayenbenyoussef/Medical_data_quality_pipeline
cd Medical_data_quality_pipeline
```

### 2. Create and activate virtual environment

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements/base.txt
```

### 4. Configure environment variables

**Windows (Command Prompt):**
```cmd
copy .env.input .env
```

**Linux/Mac:**
```bash
cp .env.input .env
```

Fill in your credentials — same variables as the Docker setup above,
but use DB_HOST=localhost and PROJECT_ROOT=your absolute project path.

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

## Running the Pipeline (Local)

### Full pipeline

Runs all steps in order: load raw → validate raw → dbt run → dbt test → extract → validate mart

```bash
python src/main.py
```

### Individual steps

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
dbt run --select path:models/staging
dbt run --select path:models/marts
```

---

## Running Tests

### Install test dependencies

```bash
pip install -r requirements/dev.txt
```

### Python unit tests (no database needed)

```bash
python -m pytest tests/ -v -m "not integration"
```

### Python integration tests (requires database)

```bash
python -m pytest tests/ -v -m integration
```

### All tests

```bash
python -m pytest tests/ -v
```

### dbt tests only

```bash
cd dbt
dbt test
```

---

## Data Flow

```
CSV files (MIMIC-IV-ED)
    |
[CSVRawLoader] — pandas reads CSV, inserts to PostgreSQL with transaction safety
    |
raw.* (PostgreSQL) — untouched source data
    |
[RawLoadValidator] — checks row counts, column counts, required nulls
    |
[dbt staging] — casts types, renames columns, handles NULLs, standardizes values
    |
stg.* (PostgreSQL) — clean, typed, standardized data
    |
[dbt marts] — builds star schema (dimensions + facts + bridge tables)
    |
mrt.* (PostgreSQL) — analytics-ready dimensional model
    |
[dbt test] — 166 data quality tests across all models
    |
[MartExtractor] — reads mart tables into pandas DataFrames
    |
[MartValidator] — Pandera schema validation on extracted DataFrames
    |
[Grafana] — real-time dashboards connecting directly to mart tables
```

---

## Airflow DAGs

| DAG | Schedule | Description |
|---|---|---|
| medical_etl_init | Manual only | Full pipeline: load all CSVs, dbt staging, dbt marts |
| medical_etl_daily | Daily at midnight | Refresh mart layer from updated staging data |
| data_quality_dag | Every minute | Run dbt tests and Pandera mart validation |

---

## Grafana Setup

Grafana connects directly to your PostgreSQL mart tables.

1. Go to http://localhost:3000
2. Login: admin / admin
3. Navigate to Dashboards to see pre-built dashboards:
   - Main Dashboard — admission analytics, LOS by acuity, visit patterns
   - Vitalsign Dashboard — per-patient vital sign time series with patient filter

To add the PostgreSQL data source manually:
- Host: postgres:5432
- Database: your DB_NAME value
- User/Password: from your .env
- TLS/SSL: disable for local development

---

## Troubleshooting

**ModuleNotFoundError: No module named config**
Run from project root, not from inside src/. Or check that pytest.ini has pythonpath = src.

**pytest not recognized**
Use python -m pytest instead of bare pytest on Windows.

**dbt debug fails**
Check your .env credentials and make sure PostgreSQL is running and schemas exist.

**Docker containers not starting**
Ensure Docker Desktop is running and you have at least 4GB RAM allocated.

**Airflow DAG import errors**
Make sure src/ is mounted as a volume in docker-compose.yml and PYTHONPATH=/opt/airflow/src is set in environment.