select
    subject_id::INT as patient_id,
    stay_id::INT,
    {{ between_nulling(fahr_to_celsius('temperature'),12,43) }}  as temperature,
    heartrate as heart_rate,
    resprate as resp_rate,
    {{ between_nulling('o2sat',50,100) }} as o2_saturation,
    {{ between_nulling('sbp',30,320) }} as systolic_bp,
    {{ between_nulling('dbp',10,200) }} as diastolic_bp,
    {{ pain_filter('pain') }}::INT as pain_level,
    {{ patient_status('pain') }} as patient_status,
    acuity::INT as acuity_level,
    chiefcomplaint as chief_complaint
from {{ source('raw','triage') }}