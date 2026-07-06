# tests/conftest.py
import pytest
from unittest.mock import MagicMock

from pandas import DataFrame

from db_connection.connectors.postgres import PostgresSqlDBConnection
from db_connection.writer import DBWriter
from config.Config import ConfigManager
from load.load_to_raw import CSVRawLoader

def mock_config():
    config = MagicMock(spec=ConfigManager)
    

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
def test_df():
    return DataFrame({
        "subject_id": [1, 2, 3],
        "stay_id": [100, 200, 300],
        "seq_num": [1, 1, 4],
        "icd_code": ["EA1", "EB1", "AZ23"],
        "icd_title": ["Hypertension", "Diabetes", "Asthma"]
    })