from db_connection.base import BaseDBConnection
from dotenv import load_dotenv
class DBReader:
    def __init__(self, db: BaseDBConnection):
        self.db = db

    def read(self, query: str) -> list:
        self.db.connect()
        try:
            self.db.execute(query)
            rows = self.db.fetchall()
            return [dict(row) for row in rows]
        finally:
            self.db.close()