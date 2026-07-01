

select
    ROW_NUMBER() OVER (ORDER by p.stay_id,p.med_row_num,p.gs_num)::INT as dispensing_id,
    p.stay_id,
    p.chart_time::DATE as dispensing_date,
    TO_CHAR(
        TIME '00:00' + (extract(HOUR from p.chart_time) * INTERVAL '1 hour') +
        (extract(MINUTE from p.chart_time) * INTERVAL '1 minute'),
        'HH24:MI'
    ) as dispensing_hour,
    p.med_row_num as med_event_num,
    m.med_id
FROM {{ ref('stg_pyxis') }} p , {{ ref('dim_medications') }} m
where lower(p.medication_name) =lower(m.medication_name)
and p.gs_num = m.gs_num