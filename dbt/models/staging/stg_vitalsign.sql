select
    subject_id::INT as patient_id,
    stay_id::INT,
    charttime as chart_time,
    {{ between_nulling(fahr_to_celsius('temperature'),12,43) }}  as temperature,
    heartrate as heart_rate,
    resprate as resp_rate,
    {{ between_nulling('o2sat',50,100) }} as o2_saturation,
    {{ between_nulling('sbp',30,320) }} as systolic_bp,
    {{ between_nulling('dbp',10,200) }} as diastolic_bp,
    CASE
        WHEN rhythm IN ('Normal Sinus Rhythm', 'sr') THEN 'Sinus Rhythm'
        WHEN rhythm IN ('Atrial Fibrillation', 'afib') THEN 'Atrial Fibrillation'
        ELSE rhythm
    END AS card_rhythm,
    {{ pain_filter('pain') }}::INT as pain_level,
    {{ patient_status('pain') }} as patient_status
from {{ source('raw','vitalsign') }}