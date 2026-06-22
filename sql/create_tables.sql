CREATE TABLE IF NOT EXISTS weather_raw (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    timestamp TIMESTAMP,
    temperature FLOAT,
    humidity INTEGER,
    weather_description VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
