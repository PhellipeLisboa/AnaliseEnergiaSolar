-- Criação do banco de dados

CREATE DATABASE IF NOT EXISTS solar_power
CHARACTER SET utf8mb4;

USE solar_power;

-- Tabela de referência das usinas

CREATE TABLE plants (
plant_code CHAR(3) NOT NULL,
plant_id VARCHAR(7) NOT NULL,

CONSTRAINT pk_plants
PRIMARY KEY (plant_code),

CONSTRAINT uq_plants_plant_id
UNIQUE (plant_id),

CONSTRAINT uq_plants_code_id
UNIQUE (plant_code, plant_id)
);

-- Tabela de medições de geração

CREATE TABLE generation_measurements (
id VARCHAR(17) NOT NULL,
date_time DATETIME NOT NULL,
plant_id VARCHAR(7) NOT NULL,
plant_code CHAR(3) NOT NULL,
source_key VARCHAR(15) NOT NULL,
inverter_code VARCHAR(10) NOT NULL,
dc_power DOUBLE NOT NULL,
ac_power DOUBLE NOT NULL,
daily_yield DOUBLE NOT NULL,
total_yield DOUBLE NOT NULL,

CONSTRAINT pk_generation_measurements
PRIMARY KEY (id),

CONSTRAINT fk_generation_plant
FOREIGN KEY (plant_code, plant_id)
REFERENCES plants (plant_code, plant_id)
ON UPDATE CASCADE
ON DELETE RESTRICT
);

-- Tabela de medições meteorológicas

CREATE TABLE weather_measurements (
id VARCHAR(17) NOT NULL,
date_time DATETIME NOT NULL,
plant_id VARCHAR(7) NOT NULL,
plant_code CHAR(3) NOT NULL,
source_key VARCHAR(15) NOT NULL,
sensor_code VARCHAR(10) NOT NULL,
ambient_temperature DOUBLE NOT NULL,
module_temperature DOUBLE NOT NULL,
irradiation DOUBLE NOT NULL,

CONSTRAINT pk_weather_measurements
PRIMARY KEY (id),

CONSTRAINT fk_weather_plant
FOREIGN KEY (plant_code, plant_id)
REFERENCES plants (plant_code, plant_id)
ON UPDATE CASCADE
ON DELETE RESTRICT
);