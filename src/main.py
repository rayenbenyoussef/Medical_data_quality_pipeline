from pandas import read_csv

from extract.fetch_data import MartExtractor
from quality.mart_validator import MartValidator
from quality.raw_validator import RawLoadValidator
from src.config.logging_config import setup_logger
from db_connection import reader, builder, writer
from config.Config import ConfigManager
from load.load_to_raw import CSVRawLoader

logger = setup_logger()

cnfmng=ConfigManager()
config=cnfmng.get_dbconfig()

db=builder.ConnectionBuilder().build(config)

dbr=reader.DBReader(db)
dbw=writer.DBWriter(db)

schemas=cnfmng.schemas
raw_csvl=CSVRawLoader(dbw,schemas["raw"],rewrite_schema=False)

diagnosis=read_csv("./data/input/diagnosis.csv")
edstays=read_csv("./data/input/edstays.csv")
medrecon=read_csv("./data/input/medrecon.csv")
pyxis=read_csv("./data/input/pyxis.csv")
triage=read_csv("./data/input/triage.csv")
vitalsign=read_csv("./data/input/vitalsign.csv")

'''
raw_csvl.build(diagnosis,"diagnosis")
raw_csvl.build(edstays,"edstays")
raw_csvl.build(medrecon,"medrecon")
raw_csvl.build(pyxis,"pyxis")
raw_csvl.build(triage,"triage")
raw_csvl.build(vitalsign,"vitalsign")
'''

valraw=RawLoadValidator(dbr,schemas["raw"])
valraw.validate(diagnosis,"diagnosis",required_not_null_columns=['subject_id', 'stay_id', 'icd_code', 'icd_title'])
valraw.validate(edstays,"edstays",required_not_null_columns=['subject_id', 'stay_id', 'hadm_id'])
valraw.validate(medrecon,"medrecon",required_not_null_columns=['subject_id', 'stay_id'])
valraw.validate(pyxis,"pyxis",required_not_null_columns=['subject_id', 'stay_id'])
valraw.validate(triage,"triage",required_not_null_columns=['subject_id', 'stay_id'])
valraw.validate(vitalsign,"vitalsign",required_not_null_columns=['subject_id', 'stay_id'])

ex=MartExtractor(dbr,schemas["mrt"])
exv=MartValidator()

df=ex.get_ed_visits()
print(exv.validate_ed_visits(df))

df=ex.get_patients()
print(exv.validate_patients(df))

df=ex.get_vitalsigns()
print(exv.validate_vitalsigns(df))

df=ex.get_medrecon()
print(exv.validate_medrecon(df))

df=ex.get_pyxis()
print(exv.validate_pyxis(df))


