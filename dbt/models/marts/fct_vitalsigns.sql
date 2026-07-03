select
    stay_id,
    chart_time,
    temperature,
    heart_rate,
    resp_rate,
    o2_saturation,
    systolic_bp,
    diastolic_bp,
    COALESCE(card_rhythm,'unknown') as card_rhythm,
    pain_level,
    patient_status
from {{ ref('stg_vitalsign') }}
WHERE COALESCE(
    temperature,
    heart_rate,
    resp_rate,
    o2_saturation,
    systolic_bp,
    diastolic_bp
) IS NOT NULL
OR  card_rhythm IS NOT NULL
OR pain_level IS NOT NULL
OR patient_status IS NOT NULL