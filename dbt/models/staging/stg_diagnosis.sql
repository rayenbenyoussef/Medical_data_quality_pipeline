select
    subject_id::INT as patient_id,
    stay_id::INT,
    seq_num::INT as diagnosis_order,
    icd_code,
    icd_version::INT,
    icd_title
from {{ source('raw','diagnosis') }}