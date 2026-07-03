from pandas.core.interchange.dataframe_protocol import DataFrame

from db_connection.writer import DBWriter
from utils.sql_helpers import sanitize_identifier
import logging
from numpy import isnan

logger = logging.getLogger("pipeline")
class CSVRawLoader:
    def __init__(self, writer: DBWriter,schema_name:str,rewrite_schema:bool=False):
        self.writer = writer
        self.raw_schema = sanitize_identifier(schema_name)
        if rewrite_schema:
            self.writer.write(f"DROP SCHEMA {self.raw_schema};")
            self.writer.write(f"CREATE SCHEMA {self.raw_schema};")
        else:
            try:
                self.writer.write(f"CREATE SCHEMA {self.raw_schema};")
            except Exception as e:
                if f'schema "{self.raw_schema}" already exists' not in str(e):
                    raise

    def build(self, csvraw: DataFrame, table_name: str,rewrite_table=False):

        table_name: str = sanitize_identifier(table_name)

        type_map :dict = {
            "int64": "BIGINT",
            "float64": "FLOAT",
            "object": "VARCHAR(255)",
            "bool": "BIT",
            "datetime64[ns]": "DATETIME",
        }
        logger.info(f"preparing table {self.raw_schema}.{table_name}.")
        columns_sql:list = []
        for column in csvraw.columns:
            safe_col:str = sanitize_identifier(column)
            sql_type:str = type_map.get(str(csvraw[column].dtype), "VARCHAR(255)")
            columns_sql.append(f"{safe_col} {sql_type}")

        columns_part:str = ", ".join(columns_sql)
        if rewrite_table:
            self.writer.write(f"DROP TABLE IF EXISTS {self.raw_schema}.{table_name} CASCADE;")

        sql:str = f"CREATE TABLE {self.raw_schema}.{table_name} ({columns_part});"
        logger.info(f"creating table {self.raw_schema}.{table_name}.")
        try:
            self.writer.write(sql)
            logger.info(f"Table {self.raw_schema}.{table_name} created")
        except Exception as e:
            logger.error("error at creating the table",exc_info=True)
            raise e

        logger.info(f"preparing data of {self.raw_schema}.{table_name} table.")
        columns:list = [sanitize_identifier(c) for c in csvraw.columns]
        columns_part:str = ", ".join(columns)
        placeholders_part:str = ", ".join([self.writer.db.placeholder] * len(columns))


        insert_sql:str = f"INSERT INTO {self.raw_schema}.{table_name} ({columns_part}) VALUES ({placeholders_part})"
        logger.info(f"inserting data of {self.raw_schema}.{table_name} table.")
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
        logger.info(f"data of {self.raw_schema}.{table_name} table inserted.")

