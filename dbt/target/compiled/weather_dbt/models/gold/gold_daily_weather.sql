

SELECT
    city,
    DATE(timestamp) AS date,
    AVG(temperature) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature,
    AVG(humidity) AS avg_humidity,
    COUNT(*) AS readings_count
FROM "weather_db"."public"."weather_silver"
GROUP BY city, DATE(timestamp)