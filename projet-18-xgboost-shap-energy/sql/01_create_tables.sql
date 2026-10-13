DROP TABLE IF EXISTS eco2mix;
CREATE TABLE IF NOT EXISTS eco2mix(
datetime TEXT PRIMARY KEY,
consommation REAL,
production REAL
);

DROP TABLE IF EXISTS meteo;
CREATE TABLE IF NOT EXISTS meteo(
    time TEXT NOT NULL,
    ville TEXT NOT NULL,
    temperature REAL,
    precipitation REAL,
    irradiation REAL,
    vitesse_vent REAL,
    humidity REAL,
    pression_atm REAL,
    PRIMARY KEY(time,ville)
);

CREATE INDEX IF NOT EXISTS idx_meteo_time ON meteo(time);

CREATE INDEX IF NOT EXISTS idx_meteo_ville ON meteo(ville);
