from airflow import DAG
from datetime import datetime,timedelta

from airflow.providers.standard.operators.bash import BashOperator

import sys
import os
from dotenv import load_dotenv
load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT")

if PROJECT_ROOT is None:
    raise ValueError("Airflow .env Variable 'PROJECT_ROOT' is not set.")

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from config.Config import ConfigManager

default_args = {
    'owner': 'rayen',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

with DAG(
    dag_id="medical_etl_daily",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2021, 10, 1),
    description='Medical Data Quality Pipeline — updating marts from new staging values',
    catchup=False,
) as dag:
    cnfmng = ConfigManager()


    load_mart=BashOperator(
        task_id='load_mart',
        bash_command=f"cd {cnfmng.dbt_dir} && dbt run --select marts",
    )


