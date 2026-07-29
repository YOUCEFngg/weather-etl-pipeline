{{ config(materialized='table') }}

SELECT
    city,
    COUNT(*) AS total_readings,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature
FROM {{ source('silver', 'weather_silver') }}
GROUP BY city
