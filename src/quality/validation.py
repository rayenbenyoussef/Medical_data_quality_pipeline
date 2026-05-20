 time_regEx=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
    print(str(df[df["intime"].astype(str).str.match(time_regEx)].shape[0])+" / "+str(df.shape[0])+" in intime match the datetime format")
    print(str(df[df["outtime"].astype(str).str.match(time_regEx)].shape[0])+" / "+str(df.shape[0])+" in outime match the datetime format")
    print(str(df[df["intime"]<=df["outtime"]].shape[0])+" / "+str(df.shape[0])+" in datetime logicly correct (intime <= outtime)")
    print("=========================================================================")

df_icd=pd.read_csv(os.path.join(BASE_DIR,'data','processed','icd_mapping.csv'))

    icd_codes_in_diag = df_diagnosis['icd_code'].unique()
    icd_codes_in_mapping = df_icd['ICD Code'].values

    missing_codes = [code for code in icd_codes_in_diag if code not in icd_codes_in_mapping]
    print("Missing ICD codes:", missing_codes)
    print(f"{len(icd_codes_in_diag) - len(missing_codes)} / {len(icd_codes_in_diag)} codes match the ICD mapping")

    excluded_codes =[code for code in missing_codes if code in df_ex_icd['ICD Code'].values]
    missing_codes = list(set(missing_codes) - set(excluded_codes))
    print("Excluded ICD codes:", excluded_codes)