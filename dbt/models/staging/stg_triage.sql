select
    subject_id::INT as patient_id,
    stay_id::INT,
    {{ fahr_to_celsius('temperature') }} as temperature,
    heartrate as heart_rate,
    resprate as resp_rate,
    o2sat as o2_saturation,
    sbp as systolic_bp,
    dbp as diastolic_bp,
    {{ pain_filter('pain') }}::INT as pain_level,
    acuity::INT as acuity_level,
    chiefcomplaint as chief_complaint
from {{ source('raw','triage') }}