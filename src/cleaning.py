import pandas as pd
import os
#from utils import plotBarNulls

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

df_edstays = pd.read_csv(os.path.join(BASE_DIR,'data','raw','edstays.csv'))
df_triage = pd.read_csv(os.path.join(BASE_DIR,'data','raw','triage.csv'))
df_vitalsign = pd.read_csv(os.path.join(BASE_DIR,'data','raw','vitalsign.csv'))
df_diagnosis = pd.read_csv(os.path.join(BASE_DIR,'data','raw','diagnosis.csv'))
df_medrecon = pd.read_csv(os.path.join(BASE_DIR,'data','raw','medrecon.csv'))
df_pyxis = pd.read_csv(os.path.join(BASE_DIR,'data','raw','pyxis.csv'))

'''
    ploting the null values in each dataframe to visualize the extent of missing data

plotBarNulls(df_edstays, 'Null Count of ED Stays DataFrame')
plotBarNulls(df_triage, 'Null Count of Triage DataFrame')
plotBarNulls(df_vitalsign, 'Null Count of Vital Signs DataFrame')
plotBarNulls(df_diagnosis, 'Null Count of Diagnosis DataFrame')
plotBarNulls(df_medrecon, 'Null Count of Medication Recon DataFrame')
plotBarNulls(df_pyxis, 'Null Count of Pyxis DataFrame')

'''




print(df_edstays.head())
print(df_triage.head())
print(df_vitalsign.head())
print(df_diagnosis.head())
print(df_medrecon.head())
print(df_pyxis.head())



