from pandas import DataFrame
from quality.pandera_schemas import EdVisitsSchema, PatientsSchemas, VitalsignsSchema, DiagnosisSchema, MedreconSchema, \
    PyxisSchema
from pandera.errors import SchemaError
import logging

logger = logging.getLogger("pipeline")
class MartValidator:
    def validate_ed_visits(self, df: DataFrame,lazy=True) -> bool:
        try:
            EdVisitsSchema.validate(df,lazy=lazy)
            logger.info("fct_ed_visits passed.")
            return True
        except SchemaError as e:
            logger.error("fct_ed_visits failed.", exc_info=True)
            return False

    def validate_patients(self, df: DataFrame,lazy=True) -> bool:
        try:
            PatientsSchemas.validate(df,lazy=lazy)
            logger.info("dim_patients passed.")
            return True
        except SchemaError as e:
            logger.error("dim_patients failed.", exc_info=True)
            return False

    def validate_vitalsigns(self, df: DataFrame,lazy=True) -> bool:
        try:
            VitalsignsSchema.validate(df,lazy=lazy)
            logger.info("fct_vitalsigns passed.")
            return True
        except SchemaError as e:
            logger.error("fct_vitalsigns failed.", exc_info=True)
            return False

    def validate_diagnosis(self, df: DataFrame,lazy=True) -> bool:
        try:
            DiagnosisSchema.validate(df,lazy=lazy)
            logger.info("fct_diagnosis passed.")
            return True
        except SchemaError as e:
            logger.error("fct_diagnosis failed.", exc_info=True)
            return False

    def validate_medrecon(self, df: DataFrame,lazy=True) -> bool:
        try:
            MedreconSchema.validate(df,lazy=lazy)
            logger.info("fct_medrecon passed.")
            return True
        except SchemaError as e:
            logger.error("fct_medrecon failed.", exc_info=True)
            return False

    def validate_pyxis(self, df: DataFrame,lazy=True) -> bool:
        try:
            PyxisSchema.validate(df,lazy=lazy)
            logger.info("fct_pyxis passed.")
            return True
        except SchemaError as e:
            logger.error("fct_pyxis failed.", exc_info=True)
            return False