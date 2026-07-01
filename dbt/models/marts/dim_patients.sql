SELECT
    patient_id,
    MAX(gender) AS gender,
    COALESCE(MAX(CASE WHEN race != 'unknown' THEN race END),'unknown') AS race,
    COALESCE(MAX(CASE WHEN region != 'unknown' THEN region END),'unknown') AS region
FROM {{ ref('stg_edstays') }}
GROUP BY patient_id