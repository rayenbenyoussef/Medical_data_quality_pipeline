from airflow import DAG
from datetime import datetime,timedelta

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    'owner': 'rayen',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def load_raw_data():
    print("Loading raw data")

with DAG(
    dag_id="medical_etl_init",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2021, 10, 1),
    description='Medical Data Quality Pipeline — full init ETL run',
    catchup=False,
) as dag:

    load_raw=PythonOperator(
        task_id='load_raw',
        python_callable=load_raw_data,
    )

    load_stg=BashOperator(
        task_id='load_stg',
        bash_command="echo stg",
    )

    load_mart=BashOperator(
        task_id='load_mart',
        bash_command="echo mart",
    )

    load_raw >> load_stg >> load_mart
