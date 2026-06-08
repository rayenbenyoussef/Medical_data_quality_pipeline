from db_connection.base import BaseDBConnection
import pyodbc
from typing import Optional

from db_connection.connectors.exceptions import QueryError, DatabaseError, DatabaseConnectionError
from quality.date_validator import _validate_str

class MsSqlDBConnection(BaseDBConnection):

    def __init__(self,server:str,database:str,username:str,password:str):
        _validate_str(server, "server")
        _validate_str(database, "database")
        _validate_str(username, "username")

        self.connection: Optional[pyodbc.Connection] = None
        self.cursor:  Optional[pyodbc.Cursor] = None
        self.server: str= server
        self.database: str= database
        self.username: str= username
        self.password: str= password

    def build_connection_string(self)->str:
        return (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={self.server};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            "TrustServerCertificate=yes;"
        )

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.build_connection_string())
            self.cursor = self.connection.cursor()
        except pyodbc.Error as e:
            raise DatabaseConnectionError("Error at connecting to database") from e


    def execute(self,query:str, params=None):
        _validate_str(query, "query")
        if self.connection and self.cursor:
            try:
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
            except pyodbc.Error as e:
                raise QueryError("Failed executing query") from e
        else:
            raise DatabaseConnectionError("Connection/Cursor was not established to excute")

    def fetchall(self) -> list[pyodbc.Row]:
        if self.cursor:
            try:
                return self.cursor.fetchall()
            except pyodbc.Error as e:
                raise QueryError("Failed feteching all rows") from e
        else:
            raise DatabaseConnectionError("Cursor was not established to fetch all")

    def fetchone(self) -> Optional[pyodbc.Row]:
        if self.cursor:
            try:
                return self.cursor.fetchone()
            except pyodbc.Error as e:
                raise DatabaseError("Failed feteching one row") from e
        else:
            raise DatabaseConnectionError("Cursor was not established to fetch one")

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
            except pyodbc.Error as e:
                raise DatabaseError("Failed commit to database") from e
        else:
            raise DatabaseConnectionError("Connection was not established to commit")

    def rollback(self):
        if self.connection:
            try:
                self.connection.rollback()
            except pyodbc.Error as e:
                raise DatabaseError("Failed rollback to database") from e
        else:
            raise DatabaseConnectionError("Connection was not established to rollback")

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.connection:
            self.connection.close()
            self.connection = None




