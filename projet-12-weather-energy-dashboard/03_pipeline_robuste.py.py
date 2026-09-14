import requests
import sqlite3
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

def recup_meteo(ville,lat,long,jours=90):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : lat,
        "longitude" : long,
        "ville" : ville,
        "timezone" : "Europe/Paris",
        "hourly" : ["temperature_2m","precipitation"],
        "past_days" : jours,
        "forecast_days" : 7
    }
    response = requests.get(url,params=params)
    if response.status_code != 200: 
        raise Exception(f"Erreur de l'API: {response.status_code}")

    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df["ville"] = ville 
    return df

def fetch_toute_villes(past_days=90):
    villes = {
        "Paris" : (48.85, 2.35),
        "Lyon" : (45.75, 4.85),
        "Marseille" : (43.30, 5.40),
        "Bordeaux" : (44.84, -0.58),
        "Lille" : (50.63, 3.06),
    }
    dftotal = []
    for ville,(lat,long) in villes.items():
        try:
            df = recup_meteo(ville,lat,long,past_days)
            dftotal.append(df)
            print(f"{ville} validées")
        except Exception as e:
            print(f"{ville} : {e}")
    if not dftotal:
        raise Exception("Aucune donnée de récupérée")
    return pd.concat(dftotal,ignore_index=True)



def clean_meteo(df): 
    df = df.copy()

    df = df[df["time"] <= pd.Timestamp('now')]

    df["temperature_2m"] = (df["temperature_2m"].interpolate(method="linear"))

    df["precipitation"] = df["precipitation"].clip(lower=0)

    return df

def stockage_donnees(df,db_path="meteo_france.db"):
    connect = sqlite3.connect("meteo_france.db")
    df.to_sql("meteo_horaire",connect, if_exists="replace", index=False)

    connect.close()
    print(f"{len(df)} de lignes stockées")

def analyser(db_path="meteo_france.db"):
    connect = sqlite3.connect(db_path)
    query = """
    SELECT ville, DATE(time) AS jour,
    ROUND(AVG(temperature_2m),1) AS temperature_moyenne,
    ROUND(SUM(precipitation),1) AS precipitation_cum_mm
    FROM meteo_horaire
    GROUP BY ville,jour
    ORDER BY ville,jour
    """
    df = pd.read_sql(query,connect)
    connect.close()
    return df

df_raw = fetch_toute_villes(past_days=90)
df_clean = clean_meteo(df_raw)
stockage_donnees(df_clean)
df_analyse = analyser()
print(df_analyse.head(10))