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
    dag_id="data_quality_dag",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2021, 10, 1),
    description='Medical Data Quality Pipeline — data quality testing',
    catchup=False,
) as dag:

    test_raw=PythonOperator(
        task_id='load_raw',
        python_callable=load_raw_data,
    )

    test_stg=BashOperator(
        task_id='load_stg',
        bash_command="echo stg",
    )

    test_mart=BashOperator(
        task_id='load_mart',
        bash_command="echo mart",
    )

    test_raw >> test_stg >> test_mart
