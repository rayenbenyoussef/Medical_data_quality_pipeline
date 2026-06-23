from logging import exception

from db_connection.base import BaseDBConnection
from dotenv import load_dotenv
class DBWriter:
    def __init__(self, db: BaseDBConnection):
        self.db = db

    def write(self, query: str,params=None) -> None:
        self.db.connect()
        try:
            self.db.execute(query,params)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        finally:
            self.db.close()
