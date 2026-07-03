from typing import Optional
from db_connection.reader import DBReader
import logging
from pandas import DataFrame

from utils.sql_helpers import sanitize_identifier

logger = logging.getLogger("pipeline")

class MartExtractor:
    def __init__(self, dbr: DBReader,schema_name:str):
        self.reader = dbr
        self.schema_name = sanitize_identifier(schema_name)

    def _read(self, table_name: str, where: Optional[str] = None) -> DataFrame:
        sql= f"select * from {self.schema_name}.{table_name}"
        if where:
            sql += f" where {where}"
        logger.info(f"Extracting data from {table_name} ...")
        try:
            res =self.reader.read(sql)
            df=DataFrame(res)
            print(df.dtypes)
            logger.info(f"extracted {df.shape[0]} rows from {table_name}.")
            return df
        except Exception as e:
            logger.error(f"Failed extracting {table_name}.", exc_info=True)
            logger.warning(f"Returning empty DataFrame for {table_name} due to extraction failure.")
            return DataFrame()

    def get_ed_visits(self) -> DataFrame:
        df=self._read("fct_ed_visits")
        df["pain_level"] = df["pain_level"].astype("Int64")
        df["arrival_date"] = df["arrival_date"].astype("str")
        df["discharge_date"] = df["discharge_date"].astype("str")
        return df

    def get_patients(self) -> DataFrame:
        return self._read("dim_patients")

    def get_vitalsigns(self) -> DataFrame:
        df=self._read("fct_vitalsigns")
        df["pain_level"] = df["pain_level"].astype("Int64")
        return df

    def get_diagnosis(self) -> DataFrame:
        return self._read("fct_diagnosis")

    def get_medrecon(self) -> DataFrame:
        df=self._read("fct_medrecon")
        df["recording_date"] = df["recording_date"].astype("str")
        return df

    def get_pyxis(self) -> DataFrame:
        df=self._read("fct_pyxis")
        df["dispensing_date"] = df["dispensing_date"].astype("str")
        return df