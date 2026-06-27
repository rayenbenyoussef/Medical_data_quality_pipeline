from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class ConfigManager:
    @staticmethod
    def get_dbconfig() -> dict:
        db_type: Optional[str] = os.getenv("DB_TYPE")

        if db_type not in ("mssql", "postgres"):
            raise ValueError(f"Invalid connection type: {db_type}")

        config = {
            "type": db_type,
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }

        if db_type == "postgres":
            config["port"] = os.getenv("DB_PORT")

        return config

    @property
    def schemas(self) -> dict:
        return {
            "raw": os.getenv("RAW_SCHEMA"),
            "stg": os.getenv("STG_SCHEMA"),
            "mrt": os.getenv("MRT_SCHEMA"),
        }
