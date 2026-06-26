from pandas import read_csv
from db_connection.writer import DBWriter
from db_connection.base import BaseDBConnection
from utils.sql_helpers import sanitize_identifier
import logging
from numpy import isnan

logger = logging.getLogger("pipeline")
class CSVLoader:
    def __init__(self, db: BaseDBConnection):
        self.writer = DBWriter(db)


    def load(self, csv_path: str, table_name: str):
        csvraw = read_csv(csv_path)

        table_name: str = sanitize_identifier(table_name)

        type_map :dict = {
            "int64": "VARCHAR(255)",
            "float64": "FLOAT",
            "object": "VARCHAR(255)",
            "bool": "BIT",
            "datetime64[ns]": "DATETIME",
        }
        logger.info(f"preparing table {table_name}.")
        columns_sql:list = []
        for column in csvraw.columns:
            safe_col:str = sanitize_identifier(column)
            sql_type:str = type_map.get(str(csvraw[column].dtype), "VARCHAR(255)")
            columns_sql.append(f"{safe_col} {sql_type}")

        columns_part:str = ", ".join(columns_sql)
        sql:str = f"CREATE TABLE {table_name} ({columns_part});"
        logger.info(f"creating table {table_name}.")
        try:
            self.writer.write(sql)
            logger.info(f"Table {table_name} created")
        except Exception as e:
            logger.error("error at creating the table",exc_info=True)
            raise e

        logger.info(f"preparing data of {table_name} table.")
        columns:list = [sanitize_identifier(c) for c in csvraw.columns]
        columns_part:str = ", ".join(columns)
        placeholders_part:str = ", ".join([self.writer.db.placeholder] * len(columns))


        insert_sql:str = f"INSERT INTO {table_name} ({columns_part}) VALUES ({placeholders_part})"
        logger.info(f"inserting data of {table_name} table.")
        try:
            for i in range(csvraw.shape[0]):
                row_values = tuple(
                    None if (isinstance(v, float) and isnan(v)) else v
                    for v in csvraw.loc[i].tolist()
                )
                self.writer.write(insert_sql, params=row_values)
                logger.info(f"\tloaded {i + 1}/{csvraw.shape[0]} of the data.")
        except Exception as e:
            self.writer.db.rollback()
            logger.error(f"error at inserting data at {csvraw.loc[i].tolist()}, rolling back ...",exc_info=True)
            raise e
        logger.info(f"data of {table_name} table inserted.")
