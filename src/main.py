from pandas import read_csv
import subprocess

from extract.fetch_data import MartExtractor
from quality.mart_validator import MartValidator
from quality.raw_validator import RawLoadValidator
from src.config.logging_config import setup_logger
from db_connection import reader, builder, writer
from config.Config import ConfigManager
from load.load_to_raw import CSVRawLoader

logger = setup_logger()

def run_pipeline():

    # 1) initialization of the database
    cnfmng=ConfigManager()
    config=cnfmng.get_dbconfig()
    db=builder.ConnectionBuilder().build(config)
    dbr=reader.DBReader(db)
    dbw=writer.DBWriter(db)
    schemas=cnfmng.schemas

    # 2) initialization of the raw data loaders
    raw_loader=CSVRawLoader(dbw,schemas["raw"],rewrite_schema=False)

    diagnosis=read_csv("./data/input/diagnosis.csv")
    edstays=read_csv("./data/input/edstays.csv")
    medrecon=read_csv("./data/input/medrecon.csv")
    pyxis=read_csv("./data/input/pyxis.csv")
    triage=read_csv("./data/input/triage.csv")
    vitalsign=read_csv("./data/input/vitalsign.csv")


    # 3) building the structure and loading the data
    raw_loader.build(diagnosis,"diagnosis",rewrite_table=True)
    raw_loader.build(edstays,"edstays",rewrite_table=True)
    raw_loader.build(medrecon,"medrecon",rewrite_table=True)
    raw_loader.build(pyxis,"pyxis",rewrite_table=True)
    raw_loader.build(triage,"triage",rewrite_table=True)
    raw_loader.build(vitalsign,"vitalsign",rewrite_table=True)


    # 4) validating the loaded raw data
    raw_validator=RawLoadValidator(dbr,schemas["raw"])

    raw_validator.validate(diagnosis,"diagnosis",required_not_null_columns=['subject_id', 'stay_id', 'icd_code', 'icd_title'])
    raw_validator.validate(edstays,"edstays",required_not_null_columns=['subject_id', 'stay_id', 'hadm_id'])
    raw_validator.validate(medrecon,"medrecon",required_not_null_columns=['subject_id', 'stay_id'])
    raw_validator.validate(pyxis,"pyxis",required_not_null_columns=['subject_id', 'stay_id'])
    raw_validator.validate(triage,"triage",required_not_null_columns=['subject_id', 'stay_id'])
    raw_validator.validate(vitalsign,"vitalsign",required_not_null_columns=['subject_id', 'stay_id'])


    # 4) run dbt (staging + marts)
    subprocess.run(["dbt", "run"], cwd="./dbt", check=True)
    subprocess.run(["dbt", "test"], cwd="./dbt", check=True)


    # 5) extracting marts tables
    extractor=MartExtractor(dbr,schemas["mrt"])

    ed_visits=extractor.get_ed_visits()
    patients=extractor.get_patients()
    vitalsigns=extractor.get_vitalsigns()
    medrecon=extractor.get_medrecon()
    pyxis=extractor.get_pyxis()


    # 6) validating the extracted data
    extractor_validator=MartValidator()

    extractor_validator.validate_ed_visits(ed_visits)
    extractor_validator.validate_patients(patients)
    extractor_validator.validate_vitalsigns(vitalsigns)
    extractor_validator.validate_medrecon(medrecon)
    extractor_validator.validate_pyxis(pyxis)

if __name__ == "__main__":
    run_pipeline()

