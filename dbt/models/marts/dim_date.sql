WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2110-01-01' as date)",
        end_date="cast('2210-01-01' as date)"
    ) }}
)

SELECT
    date_day::DATE AS full_date,
    TRIM(LOWER(TO_CHAR(date_day, 'Day'))) AS weekday_name,
    TRIM(LOWER(TO_CHAR(date_day, 'Month'))) AS month_name,
    EXTRACT(YEAR FROM date_day) AS date_year,
    CASE
        WHEN EXTRACT(MONTH FROM date_day) IN (12, 1, 2) THEN 'winter'
        WHEN EXTRACT(MONTH FROM date_day) IN (3, 4, 5) THEN 'spring'
        WHEN EXTRACT(MONTH FROM date_day) IN (6, 7, 8) THEN 'summer'
        ELSE 'fall'
    END AS date_season
FROM date_spine