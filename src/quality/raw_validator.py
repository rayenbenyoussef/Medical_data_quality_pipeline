# src/quality/raw_validator.py
from pandas import read_csv
import logging
from db_connection.reader import DBReader
from utils.sql_helpers import sanitize_identifier

logger = logging.getLogger("pipeline")

class RawLoadValidator:
    def __init__(self, reader: DBReader):
        self.reader = reader

    def validate(self, csvraw:str, table_name: str, required_not_null_columns: list[str] = None):
        orgcsv=read_csv(csvraw)
        table_name=sanitize_identifier(table_name)

        sql=f"select count(*) as cnt from {table_name};"
        res:list[dict]=self.reader.read(sql)

        if int(res[0]["cnt"])!=orgcsv.shape[0]:
            logger.warning(f"table '{table_name}' has {orgcsv.shape[0]-int(res[0]["cnt"])} missing rows")
        else:
            logger.info(f"table '{table_name}' has no missing rows")

        sql = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ;"
        rescol :list[str]=[x["column_name"] for x in self.reader.read(sql)]
        if orgcsv.shape[1]!=len(rescol):
            logger.warning(f"table '{table_name}' has {orgcsv.shape[1]-len(rescol)} missing columns")
        else:
            logger.info(f"table '{table_name}' has no missing columns")

        if required_not_null_columns:
            logger.info(f"checking {", ".join(required_not_null_columns)}' of '{table_name}' for nulls.")
            for x in required_not_null_columns:
                xn=sanitize_identifier(x)
                if x not in rescol:
                    logger.warning(f"column {x} not in table {table_name}")
                else:
                    sql = f"select count(*) as cnt from {table_name} where {x} is null or {x} = 'NaN';"
                    res:list[dict]=self.reader.read(sql)
                    if int(res[0]["cnt"])!=0:
                        logger.warning(f"\tcolumn '{x}' has {res[0]["cnt"]} null values")
                    else:
                        logger.info(f"\tcolumn '{x}' has no null values")
