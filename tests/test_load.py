import pytest
from load.load_to_raw import CSVRawLoader


class TestCsvRawLoader:

    def test_invalid_schema_name(self,mock_writer):
        with pytest.raises(ValueError):
            CSVRawLoader(mock_writer, "raw'=")

    def test_init_loader(self,mock_writer):
        loader=CSVRawLoader(mock_writer,"raw")
        assert loader.writer is mock_writer
        assert loader.raw_schema == "raw"

    def test_init_no_rewrite(self,mock_writer):
        loader=CSVRawLoader(mock_writer,"raw",rewrite_schema=False)
        calls:list[str] = [c.args[0] for c in mock_writer.write.call_args_list]

        assert calls == ["CREATE SCHEMA IF NOT EXISTS raw;"]

    def test_init_with_rewrite(self,mock_writer):
        loader=CSVRawLoader(mock_writer,"raw",rewrite_schema=True)
        calls:list[str] = [c.args[0] for c in mock_writer.write.call_args_list]

        assert calls == [
            "DROP SCHEMA IF EXISTS raw CASCADE;",
            "CREATE SCHEMA IF NOT EXISTS raw;"
        ]

    def test_load_build_no_rewrite(self,mock_writer,test_df):
        loader=CSVRawLoader(mock_writer,"raw")
        mock_writer.write.reset_mock()
        loader.build(test_df,"diagnosis",rewrite_table=False)

        calls:list[str] = [c.args[0] for c in mock_writer.write.call_args_list]

        assert sum("CREATE TABLE raw.diagnosis" in c for c in calls) == 1
        assert sum("INSERT INTO raw.diagnosis" in c for c in calls) == test_df.shape[0]

    def test_load_build_with_rewrite(self,mock_writer,test_df):
        loader=CSVRawLoader(mock_writer,"raw")
        mock_writer.write.reset_mock()
        loader.build(test_df,"diagnosis",rewrite_table=True)

        calls:list[str] = [c.args[0] for c in mock_writer.write.call_args_list]

        assert sum("DROP TABLE IF EXISTS raw.diagnosis CASCADE;" in c for c in calls) == 1
        assert sum("CREATE TABLE raw.diagnosis" in c for c in calls) == 1
        assert sum("INSERT INTO raw.diagnosis" in c for c in calls) == test_df.shape[0]


