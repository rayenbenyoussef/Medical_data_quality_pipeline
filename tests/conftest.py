# tests/conftest.py
import pytest
from unittest.mock import MagicMock

from pandas import DataFrame

from db_connection.connectors.postgres import PostgresSqlDBConnection
from db_connection.reader import DBReader
from db_connection.writer import DBWriter
from config.Config import ConfigManager

@pytest.fixture(scope="module")
def real_db():
    """Real DB connection — only for integration tests"""
    config = ConfigManager.get_dbconfig()
    db = PostgresSqlDBConnection(
        host=config["host"],
        port=config["port"],
        database=config["database"],
        username=config["user"],
        password=config["password"]
    )
    db.connect()
    yield db
    db.close()

@pytest.fixture(scope="module")
def real_reader(real_db):
    return DBReader(real_db)

@pytest.fixture
def mock_db():
    db = MagicMock(spec=PostgresSqlDBConnection)
    db.placeholder = "%s"
    db.cursor = MagicMock()
    return db

@pytest.fixture
def mock_writer(mock_db):
    writer = MagicMock(spec=DBWriter)
    writer.db=mock_db
    return writer

@pytest.fixture
def mock_reader(mock_db):
    reader = MagicMock(spec=DBReader)
    reader.db=mock_db
    return reader

@pytest.fixture
def test_df():
    return DataFrame({
        "subject_id": [1, 2, 3],
        "stay_id": [100, 200, 300],
        "seq_num": [1, 1, 4],
        "icd_code": ["EA1", "EB1", "AZ23"],
        "icd_title": ["Hypertension", "Diabetes", "Asthma"]
    })

@pytest.fixture
def test_df_patients():
    return DataFrame({
        "subject_id": [1, 2, 3],
        "name": ["ali", "sami", "ryan"],
        "lastname": ["manga", "mlawi", "vozinha"],
        "age": [13, 18, 40]
    })

@pytest.fixture
def test_df_diagnosis():
    return DataFrame({
        "stay_id": [100, 200, 300],
        "seq_num": [1, 1, 4],
        "icd_id": [2, 3, 3],
        "pain_level":[1, 10, 7],
        "arrival_date":["1-12-1234","12-3-10","11-12-2337"],
        "discharge_date":["1", "10", "7"]
    })