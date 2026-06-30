select distinct
    etc_code,
    etc_description
from {{ ref('stg_medrecon') }}
where etc_code is not null
order by etc_code