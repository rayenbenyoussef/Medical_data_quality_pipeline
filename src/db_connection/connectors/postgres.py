import psycopg
from psycopg import sql
from psycopg.rows import Row

from db_connection.base import BaseDBConnection
from typing import Optional, LiteralString
from db_connection.connectors.exceptions import QueryError, DatabaseError, DatabaseConnectionError

from quality.date_validator import _validate_str

class PostgresSqlDBConnection(BaseDBConnection):

    def __init__(self,host:str,port: str,database:str,username:str,password:str):
        super().__init__()
        _validate_str(host, "host")
        if not port.isnumeric():
            raise TypeError("Port must be a number")
        _validate_str(database, "database")
        _validate_str(username, "username")

        self.connection: Optional[psycopg.Connection] = None
        self.cursor:  Optional[psycopg.Cursor] = None
        self.host: str= host
        self.port: str= port
        self.database: str= database
        self.username: str= username
        self.password: str= password

    def build_connection_string(self)->str:
        return (
            f"postgresql://"
            f"{self.username}:{self.password}@"
            f"{self.host}:{self.port}/"
            f"{self.database}"
        )

    def connect(self):
        try:
            self.connection = psycopg.connect(conninfo=self.build_connection_string())
            self.cursor = self.connection.cursor()
        except psycopg.Error as e:
            raise DatabaseConnectionError(f"Error at connecting to database: \n{e}") from e


    def execute(self,query:LiteralString, params=None):
        _validate_str(query, "query")
        if self.connection and self.cursor:
            try:
                if params:
                    self.cursor.execute(sql.SQL(query), params)
                else:
                    self.cursor.execute(query)
            except psycopg.Error as e:
                raise QueryError(f"Failed executing query: \n{e}") from e
        else:
            raise DatabaseConnectionError("Connection/Cursor was not established to excute")

    def fetchall(self) -> list[Row]:
        if self.cursor:
            try:
                return self.cursor.fetchall()
            except psycopg.Error as e:
                raise QueryError(f"Failed feteching all rows: \n{e}") from e
        else:
            raise DatabaseConnectionError("Cursor was not established to fetch all")

    def fetchone(self) -> Optional[Row]:
        if self.cursor:
            try:
                return self.cursor.fetchone()
            except psycopg.Error as e:
                raise DatabaseError(f"Failed feteching one row: \n{e}") from e
        else:
            raise DatabaseConnectionError("Cursor was not established to fetch one")

    def commit(self):
        if self.connection:
            try:
                self.connection.commit()
            except psycopg.Error as e:
                raise DatabaseError(f"Failed commit to database: \n{e}") from e
        else:
            raise DatabaseConnectionError("Connection was not established to commit")

    def rollback(self):
        if self.connection:
            try:
                self.connection.rollback()
            except psycopg.Error as e:
                raise DatabaseError(f"Failed rollback to database: \n{e}") from e
        else:
            raise DatabaseConnectionError("Connection was not established to rollback")

    def close(self):
        if self.cursor:
            self.cursor.close()
            self.cursor = None

        if self.connection:
            self.connection.close()
            self.connection = None