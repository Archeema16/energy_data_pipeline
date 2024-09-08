-- Evaluating the JSON file, showed location_name is not unique and property_name/property_code can be null. Hence new Serial column as PK is introduced. 
CREATE TABLE IF NOT EXISTS properties (
        id SERIAL PRIMARY KEY,
        location_name VARCHAR(255) NOT NULL,
        property_name VARCHAR(100) NULL,
        property_code VARCHAR(100) NULL
    );