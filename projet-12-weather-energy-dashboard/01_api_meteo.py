import pandas as pd
import numpy as np
import requests
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

fig1 = px.line(
    df_meteo,
    x="time",
    y="temperature_2m",
    color="ville",
    title="Graphe en ligne de la Température en fonction du temps",
    labels= {
        "time" : "Date",
        "temperature_2m" : "Temperature (°C)",
        "ville" : "Ville"
    }
)

fig1.show()

df_heatmap = df_meteo[df_meteo["ville"] == "Paris"].copy()

df_heatmap["heure"] = df_heatmap["time"].dt.hour

df_heatmap["jour"] = df_heatmap["time"].dt.date

pivot = df_heatmap.pivot_table(
    index="heure",
    values="temperature_2m",
    columns="jour",
    aggfunc="mean"
)

fig2 = px.imshow(
    pivot,
    title="Heatmap température Paris — heure x jour",
    labels={
        "x": "Jour",
        "y": "Heure",
        "color": "°C"
    },
    color_continuous_scale="RdBu_r"
)

fig2.show()

fig4 = px.box(
    df_meteo,
    x="ville",
    y="temperature_2m",
    color="ville",
    title="Distribution de la temperature par ville",
    points="outliers"
)

fig4.show()

fig5 = make_subplots(rows=2,cols=2,
    subplot_titles=(
    "Températures par ville",
    "Précipitations",
    "Vitesse du vent",
    "Couverture nuageux"),
    shared_xaxes=True)

dict_color = {
    "Paris" : "#FF0000",
    "Lyon" : "#0000FF",
    "Marseille" : "#00FF00",

}

for ville,col in dict_color.items():

    dfv = df_meteo[df_meteo["ville"] == ville]

    fig5.add_trace(
        go.Scatter(
          x = dfv["time"],
          y = dfv["temperature_2m"],
          name=ville,
          mode="lines",
          line= dict(color=col),
          legendgroup=ville,
          showlegend=False ),
        row=1, col=1
    )

    fig5.add_trace(
        go.Scatter(
            x=dfv["time"],
            y=dfv["windspeed_10m"],
            name=ville,
            mode="lines",
            line= dict(color=col, dash="dot"),
            legendgroup=ville,
            showlegend=False
        ),
        row=2, col=1
    )

    fig5.add_trace(
        go.Scatter(
            x=dfv["time"],
            y=dfv["precipitation"],
            name=ville,
            mode="lines",
            line = dict(color=col),
            legendgroup=ville,
            showlegend=False,
        ), row=1, col=2

            )

    fig5.add_trace(
        go.Scatter(
            x=dfv["time"],
            y=dfv["cloudcover"],
            name=ville,
            mode="lines",
            line = dict(color=col),
            legendgroup=ville,
            showlegend=False,
        ), row=2,col=2
    )

fig5.show()
