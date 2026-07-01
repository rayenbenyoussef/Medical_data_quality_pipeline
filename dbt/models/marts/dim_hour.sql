WITH minute_series AS (
    SELECT GENERATE_SERIES(0, 1439) AS minute_of_day
)

SELECT
    TO_CHAR(
        TIME '00:00' + (minute_of_day * INTERVAL '1 minute'),
        'HH24:MI'
    ) AS time_hhmm,
    (minute_of_day / 60) AS hour_num,
    (minute_of_day % 60) AS minute_num,
    CASE
        WHEN minute_of_day / 60 BETWEEN 0 AND 5 THEN 'Night'
        WHEN minute_of_day / 60 BETWEEN 6 AND 11 THEN 'Morning'
        WHEN minute_of_day / 60 BETWEEN 12 AND 17 THEN 'Afternoon'
        WHEN minute_of_day / 60 BETWEEN 18 AND 23 THEN 'Evening'
    END AS time_of_day,
    CASE
        WHEN minute_of_day / 60 BETWEEN 7 AND 18 THEN 'Business-Hours'
        ELSE 'Off-Hours'
    END AS shift_type
FROM minute_series