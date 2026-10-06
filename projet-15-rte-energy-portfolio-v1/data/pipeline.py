import sys, os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import sqlite3
import pandas as pd
from models.forecast import train
from models.anomaly import anomaly
from fetch_rte import fetch_eco2mix
from fetch_meteo import fetch_meteo
from clean import clean_rte, clean_meteo
from store import store_rte, store_meteo, DATABASE

# La base est créée à la racine du projet, là où on lance "streamlit run app/main.py"
RACINE = os.path.join(os.path.dirname(__file__), "..")
os.chdir(RACINE)

def executer_sql(fichier):
    conn = sqlite3.connect(DATABASE)
    with open(os.path.join("sql", fichier), encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.close()

def store_prevision(df_rte, periods=96*2):
    rmse, mape, forecast, modele = train(df_rte, periods=periods)

    reel = df_rte[["date_heure","consommation"]].copy()
    reel["date_heure"] = reel["date_heure"].dt.tz_localize(None)

    df = forecast[["ds","yhat","yhat_lower","yhat_upper"]].merge(reel, left_on="ds", right_on="date_heure", how="left")
    df = pd.DataFrame({
        "date_heure": df["ds"].dt.strftime("%Y-%m-%d %H:%M:%S"),
        "conso_reelle": df["consommation"],
        "conso_predite": df["yhat"].round(1),
        "lower_bound": df["yhat_lower"].round(1),
        "upper_bound": df["yhat_upper"].round(1),
        "modele": "Prophet",
        "rmse": round(rmse, 2) if rmse is not None else None,
        "mape": round(mape, 2) if mape is not None else None,
    })

    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM prevision")
    df.to_sql("prevision", conn, if_exists="append", index=False)
    conn.close()
    print(f"nombre de lignes prevision : {len(df)}")

def store_anomalies(df_rte, seuil_z=2):
    df = anomaly(df_rte, seuil_z=seuil_z)
    df = df[df["anomalie"]][["date_heure","consommation","z_score","type_anomalie","saison"]].copy()
    df["date_heure"] = df["date_heure"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["z_score"] = df["z_score"].round(2)

    conn = sqlite3.connect(DATABASE)
    conn.execute("DELETE FROM anomalies")
    df.to_sql("anomalies", conn, if_exists="append", index=False)
    conn.close()
    print(f"nombre de lignes anomalies : {len(df)}")

def pipeline(days_back=90):
    executer_sql("setup.sql")

    print("Récupération des données RTE...")
    df_rte = fetch_eco2mix(days_back=days_back)
    if df_rte is None or df_rte.empty:
        print("Aucune donnée RTE récupérée, arrêt.")
        return
    df_rte = clean_rte(df_rte)
    store_rte(df_rte)

    print("Calcul des prévisions...")
    store_prevision(df_rte)

    print("Détection des anomalies...")
    store_anomalies(df_rte)

    print("Récupération des données météo...")
    df_meteo = fetch_meteo(days_back=days_back)
    if df_meteo is None or df_meteo.empty:
        print("Aucune donnée météo récupérée, arrêt.")
        return
    store_meteo(clean_meteo(df_meteo))

    executer_sql("queries.sql")
    print(f"Base créée : {os.path.abspath(DATABASE)}")

if __name__ == "__main__":
    pipeline(days_back=90)
