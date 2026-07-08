from extract.fetch_data import MartExtractor
import pytest

class TestMartExtractor:

    def test_invalid_schema_name(self,mock_reader):
        with pytest.raises(ValueError):
            MartExtractor(mock_reader, "mrt'=")

    def test_init_extractor(self,mock_reader):
        extractor = MartExtractor(mock_reader,"mrt")
        assert extractor.schema_name == "mrt"
        assert extractor.reader is mock_reader

    def test_read_build_correct_sql(self,mock_reader):
        extractor = MartExtractor(mock_reader, "mrt")
        df2=extractor._read("dim_patients")

        mock_reader.read.assert_called_once()
        assert "select * from mrt.dim_patients" in mock_reader.read.call_args[0][0]

    def test_read_result(self,mock_reader,test_df_diagnosis,test_df_patients):
        extractor = MartExtractor(mock_reader, "mrt")

        def side_effect(sql):
            if "fct_diagnosis" in sql:
                return test_df_diagnosis
            if "dim_patients" in sql:
                return test_df_patients

        mock_reader.read.side_effect = side_effect

        assert extractor._read("fct_diagnosis").equals(test_df_diagnosis)
        assert extractor._read("dim_patients").equals(test_df_patients)

    def test_read_with_where(self,mock_reader):
        extractor = MartExtractor(mock_reader, "mrt")

        extractor._read("fct_diagnosis", where="id=1")

        sql = mock_reader.read.call_args[0][0]
        assert "where id=1" in sql

    def test_read_failure_returns_empty(self,mock_reader):
        mock_reader.read.side_effect = Exception("DB error")

        extractor = MartExtractor(mock_reader, "mrt")

        df = extractor._read("fct_diagnosis")

        assert df.empty

    def test_get_ed_visits_type_cast(self,mock_reader, test_df_ed_visits):
        mock_reader.read.return_value = test_df_ed_visits

        extractor = MartExtractor(mock_reader, "mrt")

        df = extractor.get_ed_visits()

        assert df["pain_level"].dtype == "Int64"

