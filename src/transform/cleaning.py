import pandas as pd
import os
from utils import fToC,cToF,categorize_complaint

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def clean_df_edstays(df):

    #mapping the arrival transport modes to numerical codes for easier analysis and modeling
    df_transport=[
        (1, 'Ambulance'),
        (2, 'Walk-in'),
        (3, 'Other'),
        (4, 'Unknown')
    ]
    df_transport=pd.DataFrame(df_transport, columns=['Code', 'Transport'])
    df_transport.to_csv(os.path.join(BASE_DIR,"data","processed","transport_mapping.csv"), index=False)
    df['arrival_transport'] = df['arrival_transport'].map({'AMBULANCE': 1, 'WALK IN': 2, 'OTHER': 3, 'UNKNOWN': 4})

    print(df["gender"].unique())
    df_gender=[
        (1,"M"),
        (2,"F")
    ]
    df_gender=pd.DataFrame(df_gender,columns=["Code","Gender"])
    df_gender.to_csv(os.path.join(BASE_DIR,"data","processed","gender_mapping.csv"), index=False)
    df['gender']=df['gender'].map({'M':1, 'F':2})

    print(df['race'].unique())
    df_race=[
        (1, 'EUROPEAN'),
        (2, 'MULTIPLE'),
        (3,'NORTH AMERICAN'),
        (4,'SOUTH AMERICAN'),
        (5,'AFRICAN AMERICAN')
    ]
    df_race=pd.DataFrame(df_race,columns=['Code','Race'])
    df_race.to_csv(os.path.join(BASE_DIR,"data","processed","race_mapping.csv"), index=False)
    df['race']=df['race'].map({'PATIENT DECLINED TO ANSWER':None,
                                            'UNKNOWN':None,'WHITE - OTHER EUROPEAN':1,
                                            'OTHER':None,'MULTIPLE RACE/ETHNICITY':2,
                                            'UNABLE TO OBTAIN':None,'HISPANIC/LATINO - CUBAN':3,
                                            'HISPANIC/LATINO - SALVADORAN':3,
                                            'WHITE - BRAZILIAN':4,'PORTUGUESE':1,
                                            'WHITE':None,'BLACK/AFRICAN AMERICAN':5
                                        })

    print(df['disposition'].unique())
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
    df['disposition']=df['disposition'].map({'HOME':1,'ADMITTED':2,'TRANSFER':3,'LEFT WITHOUT BEING SEEN':4,
                                            'LEFT AGAINST MEDICAL ADVICE':5,'ELOPED':6,'OTHER':7})

def clean_df_triage(df):

    df['temperature']=df['temperature'].apply(fToC)
    df['temperature']=df['temperature'].apply(lambda x: x if 10 <= x <= 47 else None)

    df['dbp']=df['dbp'].apply(lambda x: x if 30<=x<=200 else None)

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
    df['pain']=df['pain'].map({'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
                                            '13':10,'UA':None,'o':0,'unable':None,'uta':None,'Critical':8,'ett':None})

    df['chiefcomplaint']=df['chiefcomplaint'].replace('UNKNOWN-CC', None)
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
    df['chiefcomplaint'] = df['chiefcomplaint'].apply(categorize_complaint)

def clean_df_vitalsign(df):

    df['temperature']=df['temperature'].apply(fToC).apply(lambda x : x if 10<=x<=47 else None)

    df['o2sat']=df['o2sat'].apply(lambda x : x if 55<=x<=100 else None)

    df_rhythm=[
        (1, 'Sinus Tachycardia'),
        (2, 'Atrial Fibrillation'),
        (3, 'Sinus Rhythm'),
        (4, 'Paced Rhythm'),
        (5, 'Sinus Bradycardia')
    ]
    df_rhythm=pd.DataFrame(df_rhythm, columns=['Code', 'Rhythm'])
    df_rhythm.to_csv(os.path.join(BASE_DIR,"data","processed","rhythm_mapping.csv"), index=False)

    df['rhythm']=df['rhythm'].map({'Sinus Tachycardia':1,
                                                    'Atrial Fibrillation':2,
                                                        'Sinus Rhythm':3,
                                                        'Paced Rhythm':4,
                                                        'Sinus Bradycardia':5,
                                                        'Normal Sinus Rhythm':3,
                                                        'sr':3,'afib':2})
    df['pain']=df['pain'].map({'0':0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10,
                                            'UA':None,'ua':None,'unable':None,'uta':None,'Critical':8,'ett':None,
                                            'asleep':None,'sleeping':None,'sleepin':None,'sitting ':None,'sleep ':None,'sleep':None,
                                            'laying down':None,'standing ':None,'8.5':9,'u':None,'denies':None,'does not scale':None,
                                            'Unable':None,'grimace with palpation':3,'sedated':None,'uncooperative':None,'NAD':0,
                                            'UTA':None,'0/10':0,'intubated':None,'Asleep':None})
   
def clean_df_diagnosis(df, df_icd9, df_icd10, df_ex_icd9=None, df_ex_icd10=None):

    df_icd9.index = range(1, len(df_icd9) + 1)
    df_icd9.rename(columns={'CODE': 'ICD Code','LONG DESCRIPTION (VALID ICD-9 FY2026)':'Long Description'}, inplace=True)
    df_icd9.index.name = 'Code'

    df_icd9.drop(columns=['NF EXCL'], inplace=True)
    df_icd9['ICD Version']=9    

    df_icd10.index = range(1, len(df_icd10) + 1)
    df_icd10.rename(columns={'CODE': 'ICD Code','LONG DESCRIPTION (VALID ICD-10 FY2026)':'Long Description','SHORT DESCRIPTION (VALID ICD-10 FY2026)':'Short Description'}, inplace=True)
    df_icd10.index.name = 'Code'

    df_icd10.drop(columns=['NF EXCL'], inplace=True)
    df_icd10['ICD Version']=10

    df_icd=pd.concat([df_icd9, df_icd10], ignore_index=True)

    df_icd.index=range(1, len(df_icd) + 1)
    df_icd.index.name='Code'
    df_icd.to_csv(os.path.join(BASE_DIR,'data','processed','icd_mapping.csv'), index=True)

    if df_ex_icd9 is not None:
        df_ex_icd9['ICD Version'] = 9
        df_ex_icd9.rename(
            columns={'LONG DESCRIPTION (EXCLUDED FY2026 ICD-9 ALL TYPES E, L, D)': 'Long Description'},
            inplace=True
        )

    if df_ex_icd10 is not None:
        df_ex_icd10['ICD Version'] = 10
        df_ex_icd10.rename(
            columns={'LONG DESCRIPTION (EXCLUDED FY2026 ICD-10 ALL TYPES E, L, D)': 'Long Description'},
            inplace=True
        )

    dfs = []
    if df_ex_icd9 is not None:
        dfs.append(df_ex_icd9)
    if df_ex_icd10 is not None:
        dfs.append(df_ex_icd10)

    df_ex_icd = None
    if dfs:
        df_ex_icd = pd.concat(dfs, ignore_index=True)
        df_ex_icd.index = range(1, len(df_ex_icd) + 1)
        df_ex_icd.index.name = 'Code'
        df_ex_icd.rename(columns={'CODE': 'ICD Code'}, inplace=True)

    df_icd=pd.read_csv(os.path.join(BASE_DIR,'data','processed','icd_mapping.csv'))

    icd_codes_in_diag = df_diagnosis['icd_code'].unique()
    icd_codes_in_mapping = df_icd['ICD Code'].values

    missing_codes = [code for code in icd_codes_in_diag if code not in icd_codes_in_mapping]
    excluded_codes = []
    if df_ex_icd is not None:
        excluded_codes =[code for code in missing_codes if code in df_ex_icd['ICD Code'].values]
        missing_codes = list(set(missing_codes) - set(excluded_codes))

    missing_codes_lines = df[df['icd_code'].isin(missing_codes)][['icd_code','icd_title']].apply(pd.unique)
    excluded_codes_lines = df[df['icd_code'].isin(excluded_codes)][['icd_code','icd_title']].apply(pd.unique)

    missing_codes_lines['condition']=missing_codes_lines['icd_code'].apply(lambda x: x +" (unknown)")
    excluded_codes_lines['condition']=excluded_codes_lines['icd_code'].apply(lambda x: x +" (excluded)")

    missing_codes_lines.rename(columns={'icd_code': 'ICD Code', 'icd_title': 'Long Description'}, inplace=True)
    excluded_codes_lines.rename(columns={'icd_code': 'ICD Code', 'icd_title': 'Long Description'}, inplace=True)

    df_icd = pd.concat([df_icd, missing_codes_lines, excluded_codes_lines], ignore_index=True)
    df_icd.drop(columns=['Code'], inplace=True)
    df_icd.index=range(1, len(df_icd) + 1)
    df_icd.index.name='Code'
    df_icd.to_csv(os.path.join(BASE_DIR,'data','processed','icd_mapping.csv'), index=True)

    df_icd=pd.read_csv(os.path.join(BASE_DIR,'data','processed','icd_mapping.csv'))
    map_icd=dict(zip(df_icd['ICD Code'], df_icd['Code']))
    df['icd_code'] = df['icd_code'].map(map_icd)

    df.drop(columns=['icd_version'], inplace=True)
    df.drop(columns=['icd_title'], inplace=True)

    
def clean_df_medrecon(df):
    
    print(df.info())
    print("=========================================================================")

    print(df.head())
    print("=========================================================================")

def clean_df_pyxis(df):

    print(df.info())
    print("=========================================================================")

    print(df.head())
    print("=========================================================================")