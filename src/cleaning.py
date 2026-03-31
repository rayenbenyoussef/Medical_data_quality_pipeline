import pandas as pd
import os
from utils import plotBarNulls, fToC,cToF

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df_edstays = pd.read_csv(os.path.join(BASE_DIR,'data','raw','edstays.csv'))

'''
    ploting the frequancy of null values in each dataframe to visualize the extent of missing data

plotBarNulls(df_edstays, 'Null Count of ED Stays DataFrame')
plotBarNulls(df_triage, 'Null Count of Triage DataFrame')
plotBarNulls(df_vitalsign, 'Null Count of Vital Signs DataFrame')
plotBarNulls(df_diagnosis, 'Null Count of Diagnosis DataFrame')
plotBarNulls(df_medrecon, 'Null Count of Medication Recon DataFrame')
plotBarNulls(df_pyxis, 'Null Count of Pyxis DataFrame')

'''
'''
print(df_edstays.info())
print("=========================================================================")
#mapping the arrival transport modes to numerical codes for easier analysis and modeling
print(df_edstays["arrival_transport"].unique())
df_transport=[
    (1, 'Ambulance'),
    (2, 'Walk-in'),
    (3, 'Other'),
    (4, 'Unknown')
]
df_transport=pd.DataFrame(df_transport, columns=['Code', 'Transport'])
df_transport.to_csv(os.path.join(BASE_DIR,"data","processed","transport_mapping.csv"), index=False)
df_edstays['arrival_transport'] = df_edstays['arrival_transport'].map({'AMBULANCE': 1, 'WALK IN': 2, 'OTHER': 3, 'UNKNOWN': 4})
print("=========================================================================")

time_regEx=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
print(str(df_edstays[df_edstays["intime"].astype(str).str.match(time_regEx)].shape[0])+" / "+str(df_edstays.shape[0])+" in intime match the datetime format")
print(str(df_edstays[df_edstays["outtime"].astype(str).str.match(time_regEx)].shape[0])+" / "+str(df_edstays.shape[0])+" in outime match the datetime format")
print(str(df_edstays[df_edstays["intime"]<=df_edstays["outtime"]].shape[0])+" / "+str(df_edstays.shape[0])+" in datetime logicly correct (intime <= outtime)")
print("=========================================================================")

print(df_edstays["gender"].unique())
df_gender=[
    (1,"M"),
    (2,"F")
]
df_gender=pd.DataFrame(df_gender,columns=["Code","Gender"])
df_gender.to_csv(os.path.join(BASE_DIR,"data","processed","gender_mapping.csv"), index=False)
df_edstays['gender']=df_edstays['gender'].map({'M':1, 'F':2})
print("=========================================================================")

print(df_edstays['race'].unique())
df_race=[
    (1, 'EUROPEAN'),
    (2, 'MULTIPLE'),
    (3,'NORTH AMERICAN'),
    (4,'SOUTH AMERICAN'),
    (5,'AFRICAN AMERICAN')
]
df_race=pd.DataFrame(df_race,columns=['Code','Race'])
df_race.to_csv(os.path.join(BASE_DIR,"data","processed","race_mapping.csv"), index=False)
df_edstays['race']=df_edstays['race'].map({'PATIENT DECLINED TO ANSWER':None,
                                           'UNKNOWN':None,'WHITE - OTHER EUROPEAN':1,
                                           'OTHER':None,'MULTIPLE RACE/ETHNICITY':2,
                                           'UNABLE TO OBTAIN':None,'HISPANIC/LATINO - CUBAN':3,
                                           'HISPANIC/LATINO - SALVADORAN':3,
                                           'WHITE - BRAZILIAN':4,'PORTUGUESE':1,
                                           'WHITE':None,'BLACK/AFRICAN AMERICAN':5
                                    })

#plotBarNulls(df_edstays, 'Null Count of ED Stays DataFrame')
print("=========================================================================")

print(df_edstays['disposition'].unique())
df_disposition=[
    (1, 'HOME'),
    (2, 'ADMITTED'),
    (3,'TRANSFER'),
    (4,'LEFT WITHOUT BEING SEEN'),
    (5,'LEFT AGAINST MEDICAL ADVICE'),
    (6,'ELOPED'),
    (7,'OTHER'),

]
df_race=pd.DataFrame(df_race,columns=['Code','Disposition'])
df_race.to_csv(os.path.join(BASE_DIR,"data","processed","disposition_mapping.csv"), index=False)
df_edstays['disposition']=df_edstays['disposition'].map({'HOME':1,'ADMITTED':2,'TRANSFER':3,'LEFT WITHOUT BEING SEEN':4,
                                           'LEFT AGAINST MEDICAL ADVICE':5,'ELOPED':6,'OTHER':7})
print("=========================================================================")

print(df_edstays.info())
print("=========================================================================")

print(df_edstays.head())
print("=========================================================================")


df_triage = pd.read_csv(os.path.join(BASE_DIR,'data','raw','triage.csv'))

df_triage['temperature']=df_triage['temperature'].apply(fToC))
df_triage['temperature']=df_triage['temperature'].apply(lambda x: x if 10 <= x <= 47 else None)
print(df_triage['temperature'].describe())
print("=========================================================================")

print(df_triage['heartrate'].describe())
print("=========================================================================")

print(df_triage['resprate'].describe())
print("=========================================================================")

print(df_triage['o2sat'].describe())
print("=========================================================================")

print(df_triage['sbp'].describe())
print("=========================================================================")

df_triage['dbp']=df_triage['dbp'].apply(lambda x: x if 30<=x<=200 else None)
print(df_triage['dbp'].describe())
print("=========================================================================")

df_pain=[
    (0, 'No Pain'),
    (1, 'Mild Pain'),
    (2, 'Mild Pain'),
    (3, 'Moderate Pain'),
    (4, 'Moderate Pain'),
    (5, 'Moderate Pain'),
    (6, 'Severe Pain'),
    (7, 'Severe Pain'),
    (8, 'Severe Pain'),
    (9, 'Most Severe Pain'),
    (10, 'Most Severe Pain')
]

df_pain=pd.DataFrame(df_pain, columns=['Code', 'Pain Level'])
df_pain.to_csv(os.path.join(BASE_DIR,"data","processed","pain_mapping.csv"), index=False)
df_triage['pain']=df_triage['pain'].map({'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
                                         '13':10,'UA':None,'o':0,'unable':None,'uta':None,'Critical':8,'ett':None})
print(df_triage['pain'].unique())
print("=========================================================================")

print(df_triage['acuity'].unique())
print("=========================================================================")

df_triage['chiefcomplaint']=df_triage['chiefcomplaint'].replace('UNKNOWN-CC', None)
df_chiefcomplaint=[
    (1, 'Pain / Musculoskeletal'),
    (2, 'Cardiac'),
    (3, 'Respiratory'),
    (4, 'Neurologic'),
    (5, 'Infection'),
    (6, 'Psychiatric'),
    (7, 'Trauma'),
    (8, 'Gastrointestinal'),
    (9, 'Other')
]
df_chiefcomplaint=pd.DataFrame(df_chiefcomplaint, columns=['Code', 'Chief Complaint Category'])
df_chiefcomplaint.to_csv(os.path.join(BASE_DIR,"data","processed","chiefcomplaint_mapping.csv"), index=False)

def categorize_complaint(text):
    if pd.isna(text):
        return None
    text = text.lower()
    if any(x in text for x in ['pain', 'abd', 'back', 'leg', 'arm', 'hip', 'foot', 'neck']):
        return 1
    elif any(x in text for x in ['chest', 'palpitations', 'tachycardia', 'nstemi', 'hypertension']):
        return 2
    elif any(x in text for x in ['shortness of breath', 'dyspnea', 'respiratory', 'pe']):
        return 3
    elif any(x in text for x in ['stroke', 'cva', 'facial droop', 'weakness', 'altered mental status']):
        return 4
    elif any(x in text for x in ['fever', 'infection', 'sepsis', 'neutropenia']):
        return 5
    elif any(x in text for x in ['psych', 'psychiatric', 'depression', 'suicide', 'si']):
        return 6
    elif any(x in text for x in ['trauma', 'fall', 'head bleed', 'fracture', 'mvc']):
        return 7
    elif any(x in text for x in ['vomiting', 'nausea', 'diarrhea', 'abdominal distention']):
        return 8
    else:
        return 9

df_triage['chiefcomplaint'] = df_triage['chiefcomplaint'].apply(categorize_complaint)
print(df_triage['chiefcomplaint'].unique())
print("=========================================================================")

print(df_triage.info())
print("=========================================================================")

print(df_triage.head())
print("=========================================================================")

'''

df_vitalsign = pd.read_csv(os.path.join(BASE_DIR,'data','raw','vitalsign.csv'))
df_diagnosis = pd.read_csv(os.path.join(BASE_DIR,'data','raw','diagnosis.csv'))
df_medrecon = pd.read_csv(os.path.join(BASE_DIR,'data','raw','medrecon.csv'))
df_pyxis = pd.read_csv(os.path.join(BASE_DIR,'data','raw','pyxis.csv'))

timeRgEx=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
df_correcttime=df_vitalsign['charttime'].astype(str).str.match(timeRgEx)
print(str(df_correcttime.sum())+" / " +str(df_vitalsign.shape[0])+" in charttime match the datetime format")

df_vitalsign['temperature']=df_vitalsign['temperature'].apply(fToC).apply(lambda x : x if 10<=x<=47 else None)
print(df_vitalsign['temperature'].describe())
print("=========================================================================")

print(df_vitalsign['heartrate'].describe())
print("=========================================================================")

print(df_vitalsign['resprate'].describe())
print("=========================================================================")

df_vitalsign['o2sat']=df_vitalsign['o2sat'].apply(lambda x : x if 55<=x<=100 else None)
print(df_vitalsign['o2sat'].describe())
print("=========================================================================")

print(df_vitalsign['sbp'].describe())
print("=========================================================================")

print(df_vitalsign['dbp'].describe())
print("=========================================================================")


df_rhythm=[
    (1, 'Sinus Tachycardia'),
    (2, 'Atrial Fibrillation'),
    (3, 'Sinus Rhythm'),
    (4, 'Paced Rhythm'),
    (5, 'Sinus Bradycardia')
]

df_rhythm=pd.DataFrame(df_rhythm, columns=['Code', 'Rhythm'])
df_rhythm.to_csv(os.path.join(BASE_DIR,"data","processed","rhythm_mapping.csv"), index=False)

df_vitalsign['rhythm']=df_vitalsign['rhythm'].map({'Sinus Tachycardia':1,
                                                   'Atrial Fibrillation':2,
                                                    'Sinus Rhythm':3,
                                                    'Paced Rhythm':4,
                                                    'Sinus Bradycardia':5,
                                                    'Normal Sinus Rhythm':3,
                                                    'sr':3,'afib':2})
print(df_vitalsign['rhythm'].unique())
print("=========================================================================")

print(df_vitalsign['pain'].unique())
print("=========================================================================")

print(df_vitalsign.info())
print("=========================================================================")

print(df_vitalsign.head())
print("=========================================================================")




