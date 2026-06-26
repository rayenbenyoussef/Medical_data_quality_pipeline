from quality.raw_validator import RawLoadValidator
from src.config.logging_config import setup_logger
from db_connection import reader, builder, writer
from config.DbConfig import DbConfig
from load.load_to_raw import CSVLoader
import pandas as pd

logger = setup_logger()

config=DbConfig().get_config()

db=builder.ConnectionBuilder().build(config)

dbr=reader.DBReader(db)
dbw=writer.DBWriter(db)
csvl=CSVLoader(db)

'''
csvl.load("./data/input/diagnosis.csv","diagnosis")
csvl.load("./data/input/edstays.csv","edstays")
csvl.load("./data/input/medrecon.csv","medrecon")
csvl.load("./data/input/pyxis.csv","pyxis")
csvl.load("./data/input/triage.csv","triage")
csvl.load("./data/input/vitalsign.csv","vitalsign")
'''

valraw=RawLoadValidator(dbr)
valraw.validate("./data/input/diagnosis.csv","diagnosis",required_not_null_columns=['subject_id', 'stay_id', 'icd_code', 'icd_title'])
valraw.validate("./data/input/edstays.csv","edstays",required_not_null_columns=['subject_id', 'stay_id', 'hadm_id'])
valraw.validate("./data/input/medrecon.csv","medrecon",required_not_null_columns=['subject_id', 'stay_id'])
valraw.validate("./data/input/pyxis.csv","pyxis",required_not_null_columns=['subject_id', 'stay_id'])
valraw.validate("./data/input/triage.csv","triage",required_not_null_columns=['subject_id', 'stay_id'])
valraw.validate("./data/input/vitalsign.csv","vitalsign",required_not_null_columns=['subject_id', 'stay_id'])



