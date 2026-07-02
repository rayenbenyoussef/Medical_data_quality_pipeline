SELECT DISTINCT
    e.patient_id
FROM {{ ref('stg_edstays') }} e
LEFT JOIN {{ ref('dim_patients') }} dp
    ON e.patient_id = dp.patient_id
WHERE dp.patient_id IS NULL