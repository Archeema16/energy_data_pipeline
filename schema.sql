-- Evaluating the JSON file, showed location_name is not unique and property_name/property_code can be null. Hence new Serial column as PK is introduced. 
CREATE TABLE IF NOT EXISTS properties (
        id SERIAL PRIMARY KEY,
        location_name VARCHAR(255) NOT NULL,
        property_name VARCHAR(100) NULL,
        property_code VARCHAR(100) NULL
    );


CREATE TABLE IF NOT EXISTS properties_daily_energy (
    id SERIAL PRIMARY KEY,
    location_name VARCHAR(255) NOT NULL,
    reporting_group VARCHAR(20) NOT NULL,
    value DOUBLE PRECISION,
    unit VARCHAR(10),
    date TIMESTAMP,
    load_date DATE  DEFAULT CURRENT_DATE,
    version VARCHAR(10),
    response_error JSONB
);

CREATE INDEX IF NOT EXISTS idx_location_name ON properties_daily_energy (location_name);
CREATE INDEX IF NOT EXISTS idx_reporting_group ON properties_daily_energy (reporting_group);
CREATE INDEX IF NOT EXISTS idx_date ON properties_daily_energy (date);
CREATE INDEX IF NOT EXISTS idx_location_date ON properties_daily_energy (location_name,date);