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

{% macro patient_status(column_name) %}
    CASE
        WHEN {{ column_name }} IN ('intubated','ett','sedated','Critical')
            THEN 'unable-to-assess'
        WHEN {{ column_name }} IN ('denies','uncooperative')
            THEN 'declined'
        WHEN {{ column_name }} IN ('Asleep','asleep','sleeping','sleep','sleep ',
                                    'sleepin','laying down','sitting ','standing ')
            THEN 'asleep-or-resting'
        WHEN {{ column_name }} IN ('uta','UTA','unable','Unable','u','UA','ua',
                                    'does not scale','NAD','13')
            THEN 'not-assessed'
        ELSE NULL
    END
{% endmacro %}