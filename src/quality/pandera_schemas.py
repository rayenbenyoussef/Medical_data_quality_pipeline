from pandera.typing.pandas import Index, DataFrame, Series, Date, DateTime
from pandera.pandas import Column, DataFrameModel, Field,Timestamp

class EdVisitsSchema(DataFrameModel):
    stay_id: Series[int] = Field(nullable=False,unique=True)
    patient_id : Series[int] = Field(nullable=False)
    arrival_date : Series[str] = Field(nullable=False,str_matches=r"^\d{4}-\d{2}-\d{2}$")
    arrival_hour : Series[str] = Field(nullable=False,str_matches=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    discharge_date : Series[str] = Field(nullable=False,str_matches=r"^\d{4}-\d{2}-\d{2}$")
    discharge_hour : Series[str] = Field(nullable=False,str_matches=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    arrival_transport : Series[str] = Field(nullable=False,isin=['ambulance','walk-in','unknown'])
    is_multi_diagnosed : Series[str] = Field(nullable=False,isin=['no','yes'])
    disposition : Series[str] = Field(nullable=False,isin=['admitted','home','other','left against medical advice',
                                                           'eloped','transfer','left without being seen'])
    temperature : Series[float] = Field(nullable=True,ge=12,le=43)
    heart_rate : Series[int] = Field(nullable=True,ge=20,le=300)
    resp_rate : Series[int] = Field(nullable=True,ge=4,le=60)
    o2_saturation : Series[int] = Field(nullable=True,ge=50,le=100)
    systolic_bp : Series[int] = Field(nullable=True,ge=30,le=320)
    diastolic_bp : Series[int] = Field(nullable=True,ge=10,le=200)
    pain_level : Series[int] = Field(nullable=True,ge=0,le=10)
    patient_status : Series[str] = Field(nullable=True,isin=['unable-to-assess','declined','asleep-or-resting','not-assessed'])

class PatientsSchemas(DataFrameModel):
    patient_id : Series[int] = Field(nullable=False,unique=True)
    gender : Series[str] = Field(nullable=False,isin=['M','F'])
    race : Series[str] = Field(nullable=False,isin=[ 'white','unknown','hispanic/latino','black/african','multiple' ])
    region : Series[str] = Field(nullable=False,isin=[ 'europe','south-america','north-america','unknown' ])

class VitalsignsSchema(DataFrameModel):
    stay_id : Series[int] = Field(nullable=False)
    chart_time : Series[str] = Field(nullable=False)

    temperature: Series[float] = Field(nullable=True, ge=12, le=43)
    heart_rate: Series[int] = Field(nullable=True, ge=20, le=300)
    resp_rate: Series[int] = Field(nullable=True, ge=4, le=60)
    o2_saturation: Series[int] = Field(nullable=True, ge=50, le=100)
    systolic_bp: Series[int] = Field(nullable=True, ge=30, le=320)
    diastolic_bp: Series[int] = Field(nullable=True, ge=10, le=200)
    card_rhythm : Series[str] = Field(nullable=False,isin=["Atrial Fibrillation","Sinus Rhythm","Paced Rhythm",
                                                          "Sinus Bradycardia","Sinus Tachycardia","unknown"])
    pain_level: Series[int] = Field(nullable=True, ge=0, le=10)
    patient_status: Series[str] = Field(nullable=True,
                                        isin=['unable-to-assess', 'declined', 'asleep-or-resting', 'not-assessed'])

    class Config:
        unique = ["chart_time", "stay_id"]

class DiagnosisSchema(DataFrameModel):
    diagnosis_id : Series[int] = Field(nullable=False, unique=True)
    stay_id : Series[int] = Field(nullable=False)
    icd_id : Series[int] = Field(nullable=False)

class MedreconSchema(DataFrameModel):
    medrecon_id : Series[int] = Field(nullable=False, unique=True)
    stay_id : Series[int] = Field(nullable=False)
    recording_date : Series[str] = Field(nullable=False,str_matches=r"^\d{4}-\d{2}-\d{2}$")
    recording_hour: Series[str] = Field(nullable=False, str_matches=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    med_id : Series[int] = Field(nullable=False)

class PyxisSchema(DataFrameModel):
    dispensing_id : Series[int] = Field(nullable=False, unique=True)
    stay_id : Series[int] = Field(nullable=False)
    dispensing_date : Series[str] = Field(nullable=False,str_matches=r"^\d{4}-\d{2}-\d{2}$")
    dispensing_hour : Series[str] = Field(nullable=False, str_matches=r"^(?:[01]\d|2[0-3]):[0-5]\d$")
    med_event_num : Series[int] = Field(nullable=False)
    med_id : Series[int] = Field(nullable=False)