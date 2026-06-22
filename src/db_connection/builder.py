from typing import Optional
from db_connection.base import BaseDBConnection
from db_connection.connectors import postgres, mssql


class ConnectionBuilder:

    def build(self,config:dict) -> Optional[BaseDBConnection] :
        try:
            if config["type"] == "postgres":
                return postgres.PostgresSqlDBConnection(config["host"],config["port"],config["database"],config["user"],config["password"])
            elif config["type"] == "mssql":
                return mssql.MsSqlDBConnection(config["host"],config["database"],config["user"],config["password"])
            else:
                raise ValueError(f"Invalid connection type: {config['type']}")
        except KeyError as e:
            raise KeyError(f"Invalid connection parameter: {e}") from e