from airflow import DAG
from datetime import datetime,timedelta

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from pandas import read_csv
import sys
import os
from dotenv import load_dotenv
load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT")

if PROJECT_ROOT is None:
    raise ValueError("Airflow .env Variable 'PROJECT_ROOT' is not set.")

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from config.Config import ConfigManager
from db_connection import builder, writer
from load.load_to_raw import CSVRawLoader
default_args = {
    'owner': 'rayen',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def load_raw_data():
    cnfmng = ConfigManager()
    db_configs = cnfmng.get_dbconfig()
    db = builder.ConnectionBuilder().build(db_configs)
    dbw = writer.DBWriter(db)
    schemas = cnfmng.schemas

    raw_loader = CSVRawLoader(dbw, schemas["raw"], rewrite_schema=False)

    diagnosis = read_csv(os.path.join(cnfmng.data_input, 'diagnosis.csv'))
    edstays = read_csv(os.path.join(cnfmng.data_input,'edstays.csv'))
    medrecon = read_csv(os.path.join(cnfmng.data_input,'medrecon.csv'))
    pyxis = read_csv(os.path.join(cnfmng.data_input,'pyxis.csv'))
    triage = read_csv(os.path.join(cnfmng.data_input,'triage.csv'))
    vitalsign = read_csv(os.path.join(cnfmng.data_input,'vitalsign.csv'))

    raw_loader.build(diagnosis, "diagnosis", rewrite_table=True)
    raw_loader.build(edstays, "edstays", rewrite_table=True)
    raw_loader.build(medrecon, "medrecon", rewrite_table=True)
    raw_loader.build(pyxis, "pyxis", rewrite_table=True)
    raw_loader.build(triage, "triage", rewrite_table=True)
    raw_loader.build(vitalsign, "vitalsign", rewrite_table=True)

with DAG(
    dag_id="medical_etl_init",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2021, 10, 1),
    description='Medical Data Quality Pipeline — full init ETL run',
    catchup=False,
) as dag:
    cnfmng = ConfigManager()
    load_raw=PythonOperator(
        task_id='load_raw',
        python_callable=load_raw_data,
    )

    load_stg=BashOperator(
        task_id='load_stg',
        bash_command=f"cd {cnfmng.dbt_dir} && dbt run --select staging",
    )

    load_mart=BashOperator(
        task_id='load_mart',
        bash_command=f"cd {cnfmng.dbt_dir} && dbt run --select marts",
    )

    load_raw >> load_stg >> load_mart
