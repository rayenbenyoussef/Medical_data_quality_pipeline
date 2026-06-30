WITH date_spine AS (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2110-01-01' as date)",
        end_date="cast('2210-01-01' as date)"
    ) }}
)

SELECT
    ROW_NUMBER() OVER (ORDER BY date_day)::INT AS date_id,
    date_day::DATE AS full_date,
    TO_CHAR(date_day, 'Day') AS weekday_name,
    TO_CHAR(date_day, 'Month') AS month_name,
    EXTRACT(YEAR FROM date_day) AS date_year,
    CASE
        WHEN EXTRACT(MONTH FROM date_day) IN (12, 1, 2) THEN 'Winter'
        WHEN EXTRACT(MONTH FROM date_day) IN (3, 4, 5) THEN 'Spring'
        WHEN EXTRACT(MONTH FROM date_day) IN (6, 7, 8) THEN 'Summer'
        ELSE 'Fall'
    END AS date_season
FROM date_spine