from src.config.logging_config import setup_logger
from db_connection import reader, builder, writer
from config.DbConfig import DbConfig

logger = setup_logger()

config=DbConfig().get_config()

db=builder.ConnectionBuilder().build(config)

dbr=reader.DBReader(db)
dbw=writer.DBWriter(db)
dbw.write("update patients  set first_name =%s where patient_id=%s;",("rayen",1))
res = dbr.read("SELECT * FROM patients")
print(res)
