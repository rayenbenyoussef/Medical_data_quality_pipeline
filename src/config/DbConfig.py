from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

class DbConfig:
    @staticmethod
    def get_config()->dict:
        db_type: Optional[str] = os.getenv("DB_TYPE")
        if db_type=="mysql":
            return {"type":"mysql","host":os.getenv("DB_HOST"),
                    "database":os.getenv("DB_NAME"),"user":os.getenv("DB_USER"),
                    "password":os.getenv("DB_PASSWORD")}
        elif db_type=="postgres":
            return {"type":"postgres","host":os.getenv("DB_HOST"),"port":os.getenv("DB_PORT"),
                    "database":os.getenv("DB_NAME"),"user":os.getenv("DB_USER"),
                    "password":os.getenv("DB_PASSWORD")}
        else:
            raise ValueError(f"Invalid connection type: {db_type}")
