WITH combined_medications AS (
    SELECT DISTINCT
        TRIM(LOWER(medication_name)) as medication_name,
        ndc,
        gs_num,
        etc_code
    FROM {{ ref('stg_medrecon') }}

    UNION

    SELECT DISTINCT
        TRIM(LOWER(medication_name)) as medication_name,
        NULL::BIGINT as ndc,
        gs_num,
        NULL::INT as etc_code
    FROM {{ ref('stg_pyxis') }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY medication_name, gs_num) AS med_id,
    medication_name,
    gs_num,
    MAX(ndc) AS ndc,
    MAX(etc_code) AS etc_code
FROM combined_medications
GROUP BY medication_name, gs_num
