from db_connection.base import BaseDBConnection
class DBReader:
    def __init__(self, db: BaseDBConnection):
        self.db = db

    def read(self, query: str,params=None) -> list:
        result: list[dict] = []
        self.db.connect()
        try:
            self.db.execute(query,params)
            rows: list = self.db.fetchall()
            desc: tuple[tuple] =self.db.cursor.description
            for row in rows:
                rowres : dict=dict()
                for key, value in enumerate(row):
                    rowres[desc[key][0]] = str(value)
                result.append(rowres)
            return result
        finally:
            self.db.close()