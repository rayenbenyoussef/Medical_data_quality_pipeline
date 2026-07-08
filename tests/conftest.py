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
def test_df_ed_visits():
    return DataFrame({
        "stay_id": [100, 200, 300],
        "patient_id": [1, 2, 3],
        "arrival_date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "arrival_hour": ["08:30", "13:15", "21:45"],
        "discharge_date": ["2024-01-01", "2024-01-02", "2024-01-04"],
        "discharge_hour": ["10:30", "15:00", "00:15"],
        "arrival_transport": ["ambulance", "walk-in", "unknown"],
        "is_multi_diagnosed": ["yes", "no", "yes"],
        "disposition": ["home", "admitted", "transfer"],
        "temperature": [36.7, 37.5, 38.1],
        "heart_rate": [80, 92, 110],
        "resp_rate": [18, 20, 22],
        "o2_saturation": [98, 97, 95],
        "systolic_bp": [120, 135, 145],
        "diastolic_bp": [80, 85, 90],
        "pain_level": [1, 10, 7],
        "patient_status": ["declined", "unable-to-assess", "asleep-or-resting"],
    })


@pytest.fixture
def test_df_patients():
    return DataFrame({
        "patient_id": [1, 2, 3],
        "gender": ["M", "F", "M"],
        "race": ["white", "black/african", "unknown"],
        "region": ["europe", "north-america", "unknown"],
    })


@pytest.fixture
def test_df_vitalsigns():
    return DataFrame({
        "stay_id": [100, 100, 200],
        "chart_time": [
            "2024-01-01 08:30",
            "2024-01-01 09:00",
            "2024-01-02 13:15",
        ],
        "temperature": [36.7, 37.1, 38.0],
        "heart_rate": [80, 82, 105],
        "resp_rate": [18, 19, 22],
        "o2_saturation": [98, 97, 96],
        "systolic_bp": [120, 122, 140],
        "diastolic_bp": [80, 81, 88],
        "card_rhythm": [
            "Sinus Rhythm",
            "Sinus Rhythm",
            "Atrial Fibrillation",
        ],
        "pain_level": [2, 3, 5],
        "patient_status": [
            "declined",
            "declined",
            "unable-to-assess",
        ],
    })


@pytest.fixture
def test_df_diagnosis():
    return DataFrame({
        "diagnosis_id": [1, 2, 3],
        "stay_id": [100, 200, 300],
        "icd_id": [10, 20, 30],
    })


@pytest.fixture
def test_df_medrecon():
    return DataFrame({
        "medrecon_id": [1, 2, 3],
        "stay_id": [100, 200, 300],
        "recording_date": [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
        ],
        "recording_hour": [
            "08:30",
            "10:15",
            "18:45",
        ],
        "med_id": [101, 102, 103],
    })


@pytest.fixture
def test_df_pyxis():
    return DataFrame({
        "dispensing_id": [1, 2, 3],
        "stay_id": [100, 200, 300],
        "dispensing_date": [
            "2024-01-01",
            "2024-01-02",
            "2024-01-03",
        ],
        "dispensing_hour": [
            "08:40",
            "10:20",
            "18:50",
        ],
        "med_event_num": [1001, 1002, 1003],
        "med_id": [101, 102, 103],
    })