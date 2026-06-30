SELECT
    patient_id,
    MAX(gender) AS gender,
    MAX(CASE WHEN race != 'unknown' THEN race END) AS race,
    MAX(CASE WHEN region != 'unknown' THEN region END) AS region
FROM {{ ref('stg_edstays') }}
GROUP BY patient_id