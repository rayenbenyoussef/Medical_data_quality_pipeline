from src.config.logging_config import setup_logger
from db_connection import reader,builder
from config.DbConfig import DbConfig

logger = setup_logger()

config=DbConfig().get_config()

db=builder.ConnectionBuilder().build(config)

dbr=reader.DBReader(db)

res=dbr.read("select * from test")
print(res)
