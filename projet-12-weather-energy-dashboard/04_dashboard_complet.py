import streamlit as st
import pandas as pd 
import numpy as pd
import requests
from datetime import datetime
import plotly.express as px

st.set_page_config(
    page_icon="🌤️",
    page_title="Dashboard des données API",
    layout="wide"
)

def recup_api(ville,lat,long):
    url="https://api.open-meteo.com/v1/forecast"

    params={
        "ville" : ville,
        "timezone" : "Paris/Europe",
        "latitude" : lat,
        "longitude" : long,
        "hourly" : ["temperature_2m","precipitation","windspeed_10m"],
        "past_days" : 30,
        "forecast_days" : 7
    }
    response = requests.get(url,params=params)
    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(data["hourly"])
    df["time"] = df.to_datetime(df["time"])
    df["ville"] = ville
    return df

cor_ville = {
    "Paris" : (48.85,2.18),
    "Lyon" : (45.73,4.81),
    "Marseille" : (43.27,5.37),
}

st.sidebar.title("Paramètres")

ville_choisie = st.sidebar.multiselect("Selection des villes",list(cor_ville.keys()),default="Paris")

periode = st.periode("Barre de période (nombre de jours passés)", min_value=1,max_value=90,value=30)

with st.spinner("chargement des données"):
    dfs=[]
    for ville in cor_ville:
        lat,long = cor_ville[ville]
        df = recup_api(ville,lat,long)
        dfs.append(df)

if not dfs:
    st.warning("il faut sélectionner un site au moins")
    st.stop()

dftot = pd.concat(dfs,ignore_index=True)

maintement = pd.Timestamp('now')

df_passe = dftot[dftot["time"] <= maintement].copy()

df_passe = df_passe[df_passe["time"] >= maintement - pd.Timedelta(days=periode)]


st.title("Dashboard Météo France")

st.caption(f"Dernière mise à jour est "f"{datetime.now().strftime("%d/%m/%Y %H:%M")} ")

cols = df_passe[len(ville_choisie)]

for i, ville in enumerate(ville_choisie):
    dfv = df_passe[df_passe["ville"] == ville]

    if dfv.empty():
        continue
    temp_moy = dfv["temperature_2m"].mean()
    temp_now = dfv["temperature_2m"].iloc[-1]
    delta = temp_now - temp_moy

    col[i].metric(f"{ville}",
                    f"{temp_moy} °C",
                    f"{delta} °C vs moyenne")


                






