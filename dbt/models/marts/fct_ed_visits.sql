WITH diagnosis_counts AS (
    SELECT
        stay_id,
        COUNT(*) AS diagnosis_count
    FROM {{ ref('stg_diagnosis') }}
    GROUP BY stay_id
)

select
    e.stay_id,
    e.patient_id,
    e.ed_arrival_time::DATE as arrival_date,
    TO_CHAR(
        TIME '00:00' + (extract(HOUR from e.ed_arrival_time) * INTERVAL '1 hour') +
        (extract(MINUTE from e.ed_arrival_time) * INTERVAL '1 minute'),
        'HH24:MI'
    ) AS arrival_hour,
    e.arrival_transport,

    t.temperature,
    t.heart_rate,
    t.resp_rate,
    t.o2_saturation,
    t.systolic_bp,
    t.diastolic_bp,
    t.pain_level,
    t.patient_status,
    t.acuity_level,
    CASE
        WHEN COALESCE(dc.diagnosis_count, 0) > 1 THEN 'yes'
        ELSE 'no'
    END AS is_multi_diagnosed,

    e.disposition,
    e.ed_discharge_time::DATE as discharge_date,
    TO_CHAR(
        TIME '00:00' + (extract(HOUR from e.ed_discharge_time) * INTERVAL '1 hour') +
        (extract(MINUTE from e.ed_discharge_time) * INTERVAL '1 minute'),
        'HH24:MI'
    ) AS discharge_hour

FROM {{ ref('stg_edstays') }} e
LEFT JOIN {{ ref('stg_triage') }} t ON e.stay_id = t.stay_id
LEFT JOIN diagnosis_counts dc ON e.stay_id = dc.stay_id

