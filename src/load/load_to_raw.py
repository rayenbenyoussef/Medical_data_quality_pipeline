import pandas as pd
from db_connection.writer import DBWriter
from db_connection.base import BaseDBConnection
from utils.sql_helpers import sanitize_identifier
import logging

logger = logging.getLogger("pipeline")
class CSVLoader:
    def __init__(self, db: BaseDBConnection):
        self.writer = DBWriter(db)


    def load(self, csv_path: str, table_name: str):
        csvraw = pd.read_csv(csv_path)

        table_name = sanitize_identifier(table_name)

        type_map = {
            "int64": "BIGINT",
            "float64": "FLOAT",
            "object": "VARCHAR(255)",
            "bool": "BIT",
            "datetime64[ns]": "DATETIME",
        }
        logger.info(f"preparing table {table_name}.")
        columns_sql = []
        for column in csvraw.columns:
            safe_col = sanitize_identifier(column)
            sql_type = type_map.get(str(csvraw[column].dtype), "VARCHAR(255)")
            columns_sql.append(f"{safe_col} {sql_type}")

        columns_part = ", ".join(columns_sql)
        sql = f"CREATE TABLE {table_name} ({columns_part});"
        logger.info(f"creating table {table_name}.")
        self.writer.write(sql)
        logger.info(f"Table {table_name} created")

        logger.info(f"preparing data of {table_name} table.")
        columns = [sanitize_identifier(c) for c in csvraw.columns]
        columns_part = ", ".join(columns)
        placeholders_part = ", ".join([self.writer.db.placeholder] * len(columns))


        insert_sql = f"INSERT INTO {table_name} ({columns_part}) VALUES ({placeholders_part})"
        logger.info(f"inserting data of {table_name} table.")
        for i in range(csvraw.shape[0]):
            row_values = tuple(csvraw.loc[i].tolist())
            self.writer.write(insert_sql, params=row_values)
            logger.info(f"\tloaded {i + 1}/{csvraw.shape[0]} of the data.")
        logger.info(f"data of {table_name} table inserted.")
