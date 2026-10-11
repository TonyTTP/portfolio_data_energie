DROP TABLE IF EXISTS entsoe_load;
CREATE TABLE IF NOT EXISTS entsoe_load(
    id INTEGER PRIMARY KEY,
    datetime TEXT NOT NULL,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    conso_mw REAL,
    UNIQUE(datetime,country_code)
);


DROP TABLE IF EXISTS entsoe_generation;
CREATE TABLE IF NOT EXISTS entsoe_generation(
    id INTEGER PRIMARY KEY,
    datetime TEXT NOT NULL,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    production_type TEXT NOT NULL,
    production_mw REAL,
    UNIQUE(datetime,country_code,production_type)
);

CREATE TABLE IF NOT EXISTS entsoe_prices (
    id INTEGER PRIMARY KEY,
    datetime TEXT NOT NULL,
    country_name TEXT NOT NULL,
    country_code TEXT NOT NULL,
    price_eur_mwh REAL,
    UNIQUE(datetime, country_code)
);





