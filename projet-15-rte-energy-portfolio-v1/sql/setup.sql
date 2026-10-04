CREATE TABLE IF NOT EXISTS eco2mix (
    id INTEGER PRIMARY KEY,
    date_heure TEXT NOT NULL UNIQUE,
    consommation REAL,
    eolien REAL,
    solaire REAL,
    nucleaire REAL,
    hydraulique REAL,
    bioenergies REAL,
    taux_co2 REAL,
    heure INTEGER,
    jour_semaine INTEGER,
    type_jour TEXT,
    mois INTEGER,
    saison TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS meteo (
    id INTEGER PRIMARY KEY,
    time TEXT NOT NULL,
    ville TEXT NOT NULL,
    temperature_2m REAL,
    precipitation REAL,
    created_at TEXT DEFAULT (datetime('now', 'localtime')),
    UNIQUE (time, ville)
);

CREATE TABLE IF NOT EXISTS prevision (
    id INTEGER PRIMARY KEY,
    date_heure TEXT NOT NULL,
    conso_reelle REAL,
    conso_predite REAL,
    lower_bound REAL,
    upper_bound REAL,
    modele TEXT,
    rmse REAL,
    mape REAL,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);

CREATE TABLE IF NOT EXISTS anomalies (
    id INTEGER PRIMARY KEY,
    date_heure TEXT NOT NULL,
    consommation REAL,
    z_score REAL,
    type_anomalie TEXT,
    saison TEXT,
    created_at TEXT DEFAULT (datetime('now', 'localtime'))
);
