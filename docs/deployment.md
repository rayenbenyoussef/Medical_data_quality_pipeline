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

### 5. Install dbt packages

```bash
cd dbt
dbt deps
cd ..
```

### 6. Verify dbt connection

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
