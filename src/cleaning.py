import pandas as pd
import os
from utils import plotBarNulls

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

'''
df_triage = pd.read_csv(os.path.join(BASE_DIR,'data','raw','triage.csv'))
df_vitalsign = pd.read_csv(os.path.join(BASE_DIR,'data','raw','vitalsign.csv'))
df_diagnosis = pd.read_csv(os.path.join(BASE_DIR,'data','raw','diagnosis.csv'))
df_medrecon = pd.read_csv(os.path.join(BASE_DIR,'data','raw','medrecon.csv'))
df_pyxis = pd.read_csv(os.path.join(BASE_DIR,'data','raw','pyxis.csv'))

df_triage['temperature']=(df_triage['temperature'] - 32) * 5/9
df_triage['temperature']=df_triage['temperature'].apply(lambda x: x if 10 <= x <= 47 else None)
print(df_triage['temperature'].describe())

print("=========================================================================")

print(df_triage.info())
print("=========================================================================")

print(df_triage.head())
print("=========================================================================")





