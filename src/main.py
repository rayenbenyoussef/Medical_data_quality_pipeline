from src.config.logging_config import setup_logger
from db_connection import reader, builder, writer
from config.DbConfig import DbConfig
from load.load_to_raw import CSVLoader

logger = setup_logger()

config=DbConfig().get_config()

db=builder.ConnectionBuilder().build(config)

dbr=reader.DBReader(db)
dbw=writer.DBWriter(db)
csvl=CSVLoader(db)
csvl.load("./data/input/vitalsign.csv","vitalsign")

