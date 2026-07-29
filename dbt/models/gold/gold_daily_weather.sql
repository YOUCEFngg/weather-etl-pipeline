{{ config(materialized='table') }}

SELECT
    city,
    DATE(timestamp) AS date,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS readings_count
FROM {{ source('silver', 'weather_silver') }}
GROUP BY city, DATE(timestamp)
