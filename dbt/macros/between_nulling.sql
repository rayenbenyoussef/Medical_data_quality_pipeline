{% macro between_nulling(column_name,a,b) %}
    CASE
        WHEN {{column_name}}<{{a}} OR {{column_name}}>{{b}} THEN NULL
        ELSE {{column_name}}
    END

{% endmacro %}