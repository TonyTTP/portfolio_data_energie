import pandas as pd 
import numpy as np
import requests
import sqlite3

def recup_meteo(ville,lat,long,jours=30):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude" : lat,
        "longitude" : long,
        "hourly" : ["temperature_2m","precipitation","windspeed_10m","cloudcover"],
        "timezone" : "Europe/Paris",
        "past_days" : jours,
        "forecast_days" : 7
    }

    response= requests.get(url,params=params)
    if response.status_code != 200:
        raise Exception(f"Erreur API : {response.status_code}")

    data = response.json()

    df = pd.DataFrame(data["hourly"])

    df["time"] = pd.to_datetime(df["time"])
    df["ville"] = ville

    return df

villes = {
    "Paris" : (48.85,2.18),
    "Lyon" : (45.76,4.75),
    "Marseille" : (43.28,5.21),
}

dfs = []
    
for ville,(lat,long) in villes.items() : 

    df = recup_meteo(ville,lat,long,jours=30)

    dfs.append(df)

    print(f"{ville} : {len(df)} lignes récupérés")

df_meteo = pd.concat(dfs,ignore_index=True)

print("Information concernant le dataframe :",df_meteo.info())
print("Les première lignes sont : ",df_meteo.head())

print("le nombre de valeurs manquantes est",df_meteo.isnull().sum())


temperature_moyenne = df_meteo.groupby("ville")["temperature_2m"].mean().sort_values(ascending=False)


temperature_max = temperature_moyenne.idxmax()

print("voici la température moyenne :", temperature_moyenne)

print("voici la température la plus élevé est",temperature_max)

conn = sqlite3.connect("meteo_reelle.db")

df_meteo.to_sql("meteo_reelle",conn, if_exists="replace",index=False)

conn.close()

print("les données sont stockés dans SQlite")