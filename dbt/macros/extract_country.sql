{% macro extract_region(column_name) %}
    CASE
        WHEN {{column_name}} LIKE '%PORTUGUESE%' THEN 'europe'
        WHEN {{column_name}} LIKE '%BRAZILIAN%' THEN 'south-america'
        WHEN {{column_name}} LIKE '%SALVADORAN%' THEN 'south-america'
        WHEN {{column_name}} LIKE '%CUBAN%' THEN 'south-america'
        WHEN {{column_name}} LIKE '%AMERICAN%' THEN 'north-america'
        WHEN {{column_name}} LIKE '%EUROPEAN%' THEN 'europe'
        ELSE 'unknown'
    END
{% endmacro %}