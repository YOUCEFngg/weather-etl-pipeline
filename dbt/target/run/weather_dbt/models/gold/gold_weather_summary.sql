
  
    

  create  table "weather_db"."public_gold"."gold_weather_summary__dbt_tmp"
  
  
    as
  
  (
    

SELECT
    city,
    COUNT(*) AS total_readings,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temperature,
    MIN(temperature) AS min_temperature,
    MAX(temperature) AS max_temperature
FROM "weather_db"."public"."weather_silver"
GROUP BY city
  );
  