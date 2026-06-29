select
    subject_id::INT as patient_id,
    stay_id::INT,
    charttime::timestamp as chart_time,
    med_rn::INT as med_row_num,
    gsn_rn::INT as gsn_row_num,
    gsn::INT as gs_num

from {{ source('raw','pyxis') }}