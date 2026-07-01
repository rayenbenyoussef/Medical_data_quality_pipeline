with raw_icd_unique_values as (
    select distinct
        icd_code,
        icd_version,
        icd_title
    FROM dbt_stg.stg_diagnosis
)

select
    ROW_NUMBER() OVER (ORDER BY icd_code,icd_version)::INT as icd_id,
    icd_code,
    icd_version,
    icd_title
FROM raw_icd_unique_values