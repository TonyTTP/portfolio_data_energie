import requests
import sqlite3
import numpy as np
import pands as pd
import plotly.express as px
from datetime import datetime

def recup_meteo(ville,long,lat,jours=90):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude" : lat,
        "longitude" : longitude,
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
        "Paris" : (),
        "Lyon" : (),
        "Marseille" : (),
        "Bordeaux" : (),
        "Lille" : (),
    }
    dftotal = []
    for ville,(lat,long) in villes.items():
        try:
            df = recup_meteo(ville,lat,long,past_days)
            dftotal.append(df)
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