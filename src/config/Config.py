from typing import Optional
import os
class ConfigManager:
    def __init__(self) -> None:

        self.project_root = os.getenv('PROJECT_ROOT')

        if self.project_root is None:
            raise ValueError("Variable .env.local.local 'PROJECT_ROOT' is not set..")
        self.dbt_dir = f'{self.project_root}/dbt'
        self.data_input = f'{self.project_root}/data/input'
    @staticmethod
    def get_dbconfig() -> dict:
        db_type: Optional[str] = os.getenv("DB_TYPE")

        if db_type not in "postgres":
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
            "raw": f"{os.getenv("RAW_SCHEMA")}",
            "stg": f"dbt_{os.getenv("STG_SCHEMA")}",
            "mrt": f"dbt_{os.getenv("MRT_SCHEMA")}",
        }
