{% macro fahr_to_celsius(column_name) %}
    ROUND(({{ column_name }} - 32) * 5.0 / 9.0, 1)
{% endmacro %}