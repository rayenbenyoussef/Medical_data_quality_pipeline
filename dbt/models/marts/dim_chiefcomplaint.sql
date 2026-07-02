WITH exploded AS (
    SELECT
        stay_id,
        TRIM(lower(complaint_part)) AS complaint_part
    FROM {{ ref('stg_triage') }},
    LATERAL regexp_split_to_table(chief_complaint, ',') AS complaint_part
    WHERE chief_complaint IS NOT NULL
),

classified AS (
    SELECT DISTINCT
        complaint_part AS chief_complaint,
        CASE
            WHEN LOWER(complaint_part) LIKE '%abd pain%'
              OR LOWER(complaint_part) LIKE '%abdominal%'
              OR LOWER(complaint_part) LIKE '%epigastric%'
                THEN 'Abdominal'
            WHEN LOWER(complaint_part) LIKE '%chest pain%'
              OR LOWER(complaint_part) LIKE '%cardiac%'
              OR LOWER(complaint_part) LIKE '%palpitation%'
              OR LOWER(complaint_part) LIKE '%tachycardia%'
                THEN 'Cardiac'
            WHEN LOWER(complaint_part) LIKE '%dyspnea%'
              OR LOWER(complaint_part) LIKE '%shortness of breath%'
              OR LOWER(complaint_part) IN ('sob','resp arrest')
                THEN 'Respiratory'
            WHEN LOWER(complaint_part) LIKE '%altered mental%'
              OR LOWER(complaint_part) LIKE '%headache%'
              OR LOWER(complaint_part) LIKE '%seizure%'
              OR LOWER(complaint_part) LIKE '%dizziness%'
              OR LOWER(complaint_part) LIKE '%confusion%'
              OR LOWER(complaint_part) IN ('ich','head bleed','sdh/sah','cva')
                THEN 'Neurological'
            WHEN LOWER(complaint_part) LIKE '%s/p fall%'
              OR LOWER(complaint_part) LIKE '%mvc%'
              OR LOWER(complaint_part) LIKE '%wound%'
              OR LOWER(complaint_part) LIKE '%laceration%'
              OR LOWER(complaint_part) LIKE '%assault%'
                THEN 'Trauma'
            WHEN LOWER(complaint_part) LIKE '%psych%'
              OR LOWER(complaint_part) LIKE '%suicide%'
              OR LOWER(complaint_part) IN ('si','etoh','insomnia')
                THEN 'Psychiatric'
            WHEN LOWER(complaint_part) LIKE '%fever%'
              OR LOWER(complaint_part) LIKE '%infection%'
              OR LOWER(complaint_part) LIKE '%neutropenia%'
              OR LOWER(complaint_part) IN ('ili','?infection')
                THEN 'Infectious'
            WHEN LOWER(complaint_part) LIKE '%hyperglycemia%'
              OR LOWER(complaint_part) LIKE '%hypoglycemia%'
              OR LOWER(complaint_part) LIKE '%abnormal lab%'
              OR LOWER(complaint_part) LIKE '%dehydration%'
              OR LOWER(complaint_part) IN ('dka','anemia','elevated inr')
                THEN 'Metabolic'
            WHEN LOWER(complaint_part) IN ('brbpr','hematemesis',
                                           'coffee ground emesis',
                                           'vomiting blood')
              OR LOWER(complaint_part) LIKE '%diarrhea%'
              OR LOWER(complaint_part) LIKE '%nausea%'
              OR LOWER(complaint_part) LIKE '%n/v%'
                THEN 'GI'
            WHEN LOWER(complaint_part) LIKE '%back pain%'
              OR LOWER(complaint_part) LIKE '%leg pain%'
              OR LOWER(complaint_part) LIKE '%arm pain%'
              OR LOWER(complaint_part) LIKE '%foot pain%'
              OR LOWER(complaint_part) LIKE '%weakness%'
              OR LOWER(complaint_part) LIKE '%neck pain%'
              OR LOWER(complaint_part) LIKE '%swelling%'
                THEN 'Musculoskeletal'
            WHEN LOWER(complaint_part) LIKE '%hematuria%'
              OR LOWER(complaint_part) LIKE '%dysuria%'
              OR LOWER(complaint_part) LIKE '%urinary%'
              OR LOWER(complaint_part) IN ('clogged foley','hemodialysis')
                THEN 'Urological'
            WHEN LOWER(complaint_part) LIKE '%dvt%'
              OR LOWER(complaint_part) IN ('pe','l leg dvt')
                THEN 'Vascular'
            WHEN LOWER(TRIM(complaint_part)) = 'transfer'
                THEN 'Transfer'
            ELSE 'Other'
        END AS complaint_category
    FROM exploded
)

SELECT
    ROW_NUMBER() OVER (ORDER BY complaint_category, chief_complaint) AS complaint_id,
    chief_complaint,
    complaint_category
FROM classified