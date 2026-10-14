import sqlite3 
import pandas as pd 
import os
from pathlib import Path 
from fetch_rte import fetch_eco2mix 
from clean import clean_and_features 

DB_PATH = Path(__file__).resolve().parents[1] / "database" / "energy.db"

def init_db():
    os.makedirs(DB_PATH.parent,exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS eco2mix(
    id INTEGER PRIMARY KEY,
    date_heure TEXT NOT NULL UNIQUE,
    consommation REAL,
    nucleaire REAL,
    eolien REAL,
    solaire REAL,
    hydraulique REAL,
    bioenergies REAL,
    taux_co2 REAL,
    heure INTEGER,
    mois INTEGER,
    est_weekend INTEGER,
    est_hiver INTEGER,
    heure_sin REAL,
    heure_cos REAL,
    mois_sin REAL,
    mois_cos REAL,
    conso_lag_48h REAL,
    conso_lag_7j REAL,
    part_enr_pct REAL,
    created_at TEXT DEFAULT (datetime('now'))); 
    """)


    conn.commit()
    conn.close()

def store(df):
    conn = sqlite3.connect(DB_PATH)
    df_to_store = df.rename(columns={"part_ener_%" : "part_enr_pct"})
    cols = [
        "date_heure", "consommation", "nucleaire",
        "eolien", "solaire", "hydraulique",
        "bioenergies", "taux_co2", "heure", "mois",
        "est_weekend", "est_hiver", "heure_sin",
        "heure_cos", "mois_sin", "mois_cos",
        "conso_lag_48h", "conso_lag_7j", "part_enr_pct"]

    cols_dispo = [c for c in cols if c in df_to_store.columns]
    df_to_store = df_to_store[cols_dispo]

    df_to_store["date_heure"] = df_to_store["date_heure"].dt.tz_convert("UTC").astype(str)

    try:
        df_to_store.to_sql("eco2mix_tmp", conn,if_exists="replace",index=False)
        colonnes = ",".join(cols_dispo)
        conn.execute(f"INSERT OR IGNORE INTO eco2mix ({colonnes}) SELECT {colonnes} FROM eco2mix_tmp")
        conn.execute("DROP TABLE eco2mix_tmp")
        conn.commit()

    except Exception as e:
        print(f"Erreur store : {e}")

    finally:
        conn.close()

def load(limit=None):
    conn  = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM eco2mix ORDER BY date_heure"
    if limit:
        query += f" LIMIT {limit}"
    df    = pd.read_sql(query, conn)
    df["date_heure"] = pd.to_datetime(df["date_heure"])
    conn.close()
    print(f"{len(df)} lignes chargées")
    return df


if __name__ == "__main__":
    init_db()
    df_raw   = fetch_eco2mix(days_back=30)
    df_clean = clean_and_features(df_raw)
    store(df_clean)

    df_loaded = load(limit=5)
    print(df_loaded[["date_heure", "consommation",
                      "heure_sin"]].head())