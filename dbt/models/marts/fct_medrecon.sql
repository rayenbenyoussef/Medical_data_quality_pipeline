select
    ROW_NUMBER() OVER (ORDER by mr.stay_id,mr.medication_name,mr.gs_num,mr.ndc,mr.etc_code)::INT as medrecon_id,
    mr.stay_id,
    mr.chart_time::DATE as recording_date,
    TO_CHAR(
        TIME '00:00' + (extract(HOUR from mr.chart_time) * INTERVAL '1 hour') +
        (extract(MINUTE from mr.chart_time) * INTERVAL '1 minute'),
        'HH24:MI'
    ) as recording_hour,
    m.med_id
from {{ ref('stg_medrecon') }} mr, {{ ref('dim_medications') }} m
where lower(mr.medication_name) =lower(m.medication_name)
and mr.gs_num = m.gs_num
