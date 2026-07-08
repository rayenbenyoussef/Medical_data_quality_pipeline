
from quality.pandera_schemas import EdVisitsSchema, PatientsSchemas, VitalsignsSchema, DiagnosisSchema, MedreconSchema, \
    PyxisSchema
import pytest
from pandera.errors import SchemaError

class TestSchemas:

    def test_ed_visits_schema(self,test_df_ed_visits):
        validated = EdVisitsSchema.validate(test_df_ed_visits)

        assert validated.equals(test_df_ed_visits)

    def test_ed_visits_invalid_pain_level(self, test_df_ed_visits):
        df = test_df_ed_visits.copy()
        df.loc[0, "pain_level"] = 15

        with pytest.raises(SchemaError):
            EdVisitsSchema.validate(df)


    def test_patients_schema(self,test_df_patients):
        validated = PatientsSchemas.validate(test_df_patients)

        assert validated.equals(test_df_patients)

    def test_patients_schemas_invalid_gender(self, test_df_patients):
        df = test_df_patients.copy()
        df.loc[0, "gender"] = "A"

        with pytest.raises(SchemaError):
            PatientsSchemas.validate(df)

    def test_vitalsigns_schema(self, test_df_vitalsigns):
        validated = VitalsignsSchema.validate(test_df_vitalsigns)

        assert validated.equals(test_df_vitalsigns)

    def test_vitalsigns_schema_unique_stay_id_chart_time(self, test_df_vitalsigns):
        df = test_df_vitalsigns.copy()
        df.loc[0, "stay_id"] = 1
        df.loc[0, "chart_time"] = "2024-01-02 13:15"

        df.loc[1, "stay_id"] = 1
        df.loc[1, "chart_time"] = "2024-01-02 13:15"
        with pytest.raises(SchemaError):
            VitalsignsSchema.validate(df)

    def test_diagnosis_schema(self, test_df_diagnosis):
        validated = DiagnosisSchema.validate(test_df_diagnosis)

        assert validated.equals(test_df_diagnosis)

    def test_diagnosis_schema_unique_diagnosis_id(self, test_df_diagnosis):
        df = test_df_diagnosis.copy()
        df.loc[0, "diagnosis_id"] = 1
        df.loc[1, "diagnosis_id"] = 1
        with pytest.raises(SchemaError):
            DiagnosisSchema.validate(df)

    def test_medrecon_schema(self, test_df_medrecon):
        validated = MedreconSchema.validate(test_df_medrecon)

        assert validated.equals(test_df_medrecon)

    def test_medrecon_schema_med_id_not_null(self, test_df_medrecon):
        df = test_df_medrecon.copy()
        df.loc[0, "med_id"] = None
        with pytest.raises(SchemaError):
            MedreconSchema.validate(df)

    def test_pyxis_schema(self, test_df_pyxis):
        validated = PyxisSchema.validate(test_df_pyxis)

        assert validated.equals(test_df_pyxis)

    def test_pyxis_schema_dispensing_date_format(self, test_df_pyxis):
        df = test_df_pyxis.copy()
        df.loc[0, "dispensing_date"] = "2222/10/12"
        with pytest.raises(SchemaError):
            PyxisSchema.validate(df)