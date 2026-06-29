{% macro extract_race(column_name) %}
    CASE
        WHEN {{column_name}} LIKE '%WHITE%' THEN 'white'
        WHEN {{column_name}} LIKE '%HISPANIC/LATINO%' THEN 'hispanic/latino'
        WHEN {{column_name}} LIKE '%MULTIPLE%' THEN 'multiple'
        WHEN {{column_name}} LIKE '%BLACK/AFRICAN%' THEN 'black/african'
        ELSE 'unknown'
    END
{% endmacro %}