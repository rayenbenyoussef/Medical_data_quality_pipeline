WITH exploded AS (
    SELECT
        stay_id,
        TRIM(complaint_part) AS complaint_part
    FROM {{ ref('stg_triage') }},
    LATERAL regexp_split_to_table(chief_complaint, ',') AS complaint_part
    WHERE chief_complaint IS NOT NULL
)

SELECT
    e.stay_id,
    c.complaint_id
FROM exploded e
JOIN {{ ref('dim_chiefcomplaint') }} c
    ON TRIM(LOWER(e.complaint_part)) = TRIM(LOWER(c.chief_complaint))