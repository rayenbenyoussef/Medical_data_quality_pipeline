from db_connection.reader import DBReader
from db_connection.base import BaseDBConnection
import logging

logger = logging.getLogger("pipeline")

class MartExtractor:
    def __init__(self, db: BaseDBConnection):
        self.reader = DBReader(db)

    def get_ed_visits(self) -> list[dict]:
        # hint: query fct_ed_visits from your mart schema
        pass

    def get_patients(self) -> list[dict]:
        # hint: query dim_patients
        pass

    def get_vitalsigns(self) -> list[dict]:
        # hint: query fct_vitalsigns
        pass