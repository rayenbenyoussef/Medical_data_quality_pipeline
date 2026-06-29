select
    subject_id::INT as patient_id,
    stay_id::INT,
    {{ fahr_to_celsius('temperature') }} as temperature,
    heartrate as heart_rate,
    resprate as resp_rate,
    o2sat as o2_saturation,
    sbp as systolic_bp,
    dbp as diastolic_bp,
    CASE
        WHEN rhythm IN ('Normal Sinus Rhythm', 'sr') THEN 'Sinus Rhythm'
        WHEN rhythm IN ('Atrial Fibrillation', 'afib') THEN 'Atrial Fibrillation'
        ELSE rhythm
    END AS card_rhythm,
    {{ pain_filter('pain') }}::INT as pain_level
from {{ source('raw','vitalsign') }}