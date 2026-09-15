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
