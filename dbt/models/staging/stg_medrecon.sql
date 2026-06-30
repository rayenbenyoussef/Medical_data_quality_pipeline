select
    subject_id::INT as patient_id,
    stay_id::INT,
    charttime::timestamp as chart_time,
    name as medication_name,
    gsn::INT as gs_num,
    ndc ,
    etc_rn::INT as etc_row_num,
    etccode::INT as etc_code,
    etcdescription as etc_description
from {{ source('raw','medrecon') }}