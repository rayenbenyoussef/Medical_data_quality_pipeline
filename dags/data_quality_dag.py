from airflow import DAG
from datetime import datetime,timedelta

from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from pandas import read_csv

import sys
import os
from dotenv import load_dotenv

from extract.fetch_data import MartExtractor
from quality.mart_validator import MartValidator

load_dotenv()
PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/opt/airflow")

if PROJECT_ROOT is None:
    raise ValueError("Airflow Variable 'PROJECT_ROOT' is not set. Go to Admin → Variables and add it.")

sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from config.Config import ConfigManager
from db_connection import builder, reader
from quality.raw_validator import RawLoadValidator

default_args = {
    'owner': 'rayen',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
}

def test_raw_data():
    cnfmng = ConfigManager()
    db_configs = cnfmng.get_dbconfig()
    db = builder.ConnectionBuilder().build(db_configs)
    dbr = reader.DBReader(db)
    schemas = cnfmng.schemas

    diagnosis = read_csv(f"{cnfmng.data_input}/diagnosis.csv")
    edstays = read_csv(f"{cnfmng.data_input}/edstays.csv")
    medrecon = read_csv(f"{cnfmng.data_input}/medrecon.csv")
    pyxis = read_csv(f"{cnfmng.data_input}/pyxis.csv")
    triage = read_csv(f"{cnfmng.data_input}/triage.csv")
    vitalsign = read_csv(f"{cnfmng.data_input}/vitalsign.csv")

    raw_validator = RawLoadValidator(dbr, schemas["raw"])

    raw_validator.validate(diagnosis, "diagnosis",
                           required_not_null_columns=['subject_id', 'stay_id', 'icd_code', 'icd_title'])
    raw_validator.validate(edstays, "edstays", required_not_null_columns=['subject_id', 'stay_id', 'hadm_id'])
    raw_validator.validate(medrecon, "medrecon", required_not_null_columns=['subject_id', 'stay_id'])
    raw_validator.validate(pyxis, "pyxis", required_not_null_columns=['subject_id', 'stay_id'])
    raw_validator.validate(triage, "triage", required_not_null_columns=['subject_id', 'stay_id'])
    raw_validator.validate(vitalsign, "vitalsign", required_not_null_columns=['subject_id', 'stay_id'])


def test_pandera_mart_data():
    cnfmng = ConfigManager()
    db_configs = cnfmng.get_dbconfig()
    db = builder.ConnectionBuilder().build(db_configs)
    dbr = reader.DBReader(db)
    schemas = cnfmng.schemas

    extractor = MartExtractor(dbr, schemas["mrt"])
    ed_visits = extractor.get_ed_visits()
    patients = extractor.get_patients()
    vitalsigns = extractor.get_vitalsigns()
    medrecon = extractor.get_medrecon()
    pyxis = extractor.get_pyxis()

    extractor_validator = MartValidator()
    extractor_validator.validate_ed_visits(ed_visits)
    extractor_validator.validate_patients(patients)
    extractor_validator.validate_vitalsigns(vitalsigns)
    extractor_validator.validate_medrecon(medrecon)
    extractor_validator.validate_pyxis(pyxis)


with DAG(
    dag_id="data_quality_dag",
    default_args=default_args,
    schedule=timedelta(minutes=1),
    start_date=datetime(2021, 10, 1),
    description='Medical Data Quality Pipeline — data quality testing',
    catchup=False,
) as dag:
    cnfmng = ConfigManager()
    test_raw=PythonOperator(
        task_id='test_raw',
        python_callable=test_raw_data,
    )

    test_stg=BashOperator(
        task_id='test_stg',
        bash_command=f"cd {cnfmng.dbt_dir} && dbt test --select staging",
    )

    test_mart=BashOperator(
        task_id='test_mart',
        bash_command=f"cd {cnfmng.dbt_dir} && dbt test --select marts",
    )

    test_pandera_mart=PythonOperator(
        task_id='test_pandera_mart',
        python_callable=test_pandera_mart_data,
    )

    test_raw >> test_stg >> test_mart >> test_pandera_mart
