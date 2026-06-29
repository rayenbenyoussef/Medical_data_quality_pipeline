{% macro pain_filter(column_name) %}
    CASE
        WHEN {{ column_name }} IN ('ua','standing ','intubated','sitting ','denies','Asleep','laying down',
                                    'Unable','sleeping','u','asleep','sleep ','sleep','NAD',
                                    'sedated','UTA','sleepin','does not scale','uncooperative',
                                    'uta', 'unable', 'ett', 'Critical', '13','UA') THEN NULL
        WHEN {{ column_name }} = 'grimace with palpation' THEN '5'
        WHEN {{ column_name }} = '8.5' THEN '9'
        WHEN {{ column_name }} IN ('o','0/10') THEN '0'
        ELSE {{ column_name }}
    END
{% endmacro %}