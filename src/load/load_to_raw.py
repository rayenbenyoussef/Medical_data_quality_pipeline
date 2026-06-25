import pandas as pd
from db_connection.writer import DBWriter
from db_connection.base import BaseDBConnection
from utils.sql_helpers import sanitize_identifier

class CSVLoader:
    def __init__(self, db: BaseDBConnection):
        self.writer = DBWriter(db)


    def load(self, csv_path: str, table_name: str):
        csvraw = pd.read_csv(csv_path)

        table_name = sanitize_identifier(table_name)

        type_map = {
            "int64": "INT",
            "float64": "FLOAT",
            "object": "VARCHAR(255)",
            "bool": "BIT",
            "datetime64[ns]": "DATETIME",
        }

        columns_sql = []
        for column in csvraw.columns:
            safe_col = sanitize_identifier(column)
            sql_type = type_map.get(str(csvraw[column].dtype), "VARCHAR(255)")
            columns_sql.append(f"{safe_col} {sql_type}")

        columns_part = ", ".join(columns_sql)
        sql = f"CREATE TABLE {table_name} ({columns_part});"

        #self.writer.write(sql)
        sql = f"INSERT INTO {table_name} VALUES "
        for i in range(csvraw.shape[0]):
            rowlist=csvraw.loc[i].to_list()
            rowlist=[sanitize_identifier(str(v)) for v in rowlist]
            sql +="(" +",".join(rowlist)+") ,"
        sql = sql[:-1]
        sql+=";"
        print(sql)
