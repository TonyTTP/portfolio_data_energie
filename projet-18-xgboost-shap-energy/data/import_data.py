from datetime import date, timedelta
from pathlib import Path
import sqlite3
import requests
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "energy.db"
SQL_DIR = ROOT / "sql"

ODRE_URL = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/{}/exports/json"
METEO_URL = "https://archive-api.open-meteo.com/v1/archive"
FILIERES = ["nucleaire", "eolien", "solaire", "hydraulique", "bioenergies", "gaz", "charbon", "fioul"]

def fetch_eco2mix(debut, fin):
    dfs = []
    for dataset in ["eco2mix-national-cons-def", "eco2mix-national-tr"]:
        params = {
            "select": ",".join(["date_heure", "consommation"] + FILIERES),
            "where": f"date_heure >= '{debut}' AND date_heure < '{fin}' AND consommation IS NOT NULL",
            "order_by": "date_heure",
            "timezone": "UTC",
        }
        reponse = requests.get(ODRE_URL.format(dataset), params=params, timeout=120)
        reponse.raise_for_status()
        dfs.append(pd.DataFrame(reponse.json()))
    df = pd.concat(dfs, ignore_index=True)
    df["datetime"] = pd.to_datetime(df["date_heure"], utc=True).dt.floor("h")
    df["production"] = df[FILIERES].sum(axis=1, min_count=1)
    df = df.groupby("datetime", as_index=False)[["consommation", "production"]].mean()
    df["datetime"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")
    print(f"eco2mix : {len(df)} heures")
    return df

def fetch_meteo(debut, fin, ville="Paris", lat=48.86, lon=2.35):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": str(debut),
        "end_date": str(fin - timedelta(days=1)),
        "hourly": "temperature_2m,precipitation,shortwave_radiation,wind_speed_10m,relative_humidity_2m,pressure_msl",
        "timezone": "GMT",
    }
    reponse = requests.get(METEO_URL, params=params, timeout=120)
    reponse.raise_for_status()
    df = pd.DataFrame(reponse.json()["hourly"]).rename(columns={
        "temperature_2m": "temperature",
        "shortwave_radiation": "irradiation",
        "wind_speed_10m": "vitesse_vent",
        "relative_humidity_2m": "humidity",
        "pressure_msl": "pression_atm",
    })
    df["time"] = pd.to_datetime(df["time"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df["ville"] = ville
    print(f"météo {ville} : {len(df)} heures")
    return df[["time", "ville", "temperature", "precipitation", "irradiation", "vitesse_vent", "humidity", "pression_atm"]]

def store(df_eco2mix, df_meteo):
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript((SQL_DIR / "01_create_tables.sql").read_text(encoding="utf-8"))
        df_eco2mix.to_sql("eco2mix", conn, if_exists="append", index=False)
        df_meteo.to_sql("meteo", conn, if_exists="append", index=False)
        conn.executescript((SQL_DIR / "02_import_features.sql").read_text(encoding="utf-8"))
        nb = conn.execute("SELECT COUNT(*) FROM v_ml_features").fetchone()[0]
    print(f"Base créée : {DB_PATH} ({nb} lignes dans v_ml_features)")

if __name__ == "__main__":
    fin = date.today() - timedelta(days=7)
    debut = fin - timedelta(days=730)
    store(fetch_eco2mix(debut, fin), fetch_meteo(debut, fin))
