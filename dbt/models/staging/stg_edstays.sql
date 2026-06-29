select
    subject_id::INT as patient_id,
    stay_id::INT,
    intime::timestamp as ed_arrival_time,
    outtime::timestamp as ed_discharge_time,
    gender,
    {{ extract_race('race') }} as race,
    {{ extract_region('race') }} as region,
    CASE
        WHEN arrival_transport LIKE '%AMBULANCE%' THEN 'ambulance'
        WHEN arrival_transport LIKE '%WALK IN%' THEN 'walk-in'
        ELSE 'unknown'
    END as arrival_transport,
    LOWER(disposition) as disposition
from {{ source('raw','edstays') }}
