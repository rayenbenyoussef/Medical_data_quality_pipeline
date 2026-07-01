select
    ROW_NUMBER() OVER (ORDER by d.stay_id,d.diagnosis_order,d.icd_code)::INT as diagnosis_id,
    d.stay_id,
    dic.icd_id as icd_id
from {{ ref('stg_diagnosis') }} d , {{ ref('dim_icd_classification') }} dic
where d.icd_code=dic.icd_code
and d.icd_version=dic.icd_version