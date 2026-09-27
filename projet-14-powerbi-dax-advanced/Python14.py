from datetime import datetime, timedelta
import requests
import pandas as pd
import sqlite3


nb_jour = 30

url_national = (
    "https://data.rte-france.com"
    "/api/explore/v2.1/catalog/datasets"
    "/eco2mix-national-cons-def/records"
)

url_regional = (
    "https://data.rte-france.com"
    "/api/explore/v2.1/catalog/datasets"
    "/eco2mix-regional-tr/records"
)

def recup(url,where,size=10000):
    tout_enr = []
    offset = 0
    while True :
        params = {
            "timezone" : "Europe/Paris",
            "offset" : offset,
            "where" : where,
            "limit" : size,
            "order_by" : "date_heure ASC"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("results", [])

        if not records:
            break
        tout_enr.extend(records)
        if len(records) < size:
            break 
        offset += records

    return pd.DataFrame(tout_enr)

def temporalite(df):
    df["date_heure"] = df["date_heure"].dt.datetime
    df = df.dropna(subset="date_heure")
    df["annee"] = df["date_heure"].dt.year
    df["mois"] = df["date_heure"].dt.month
    df["jour"] = df["date_heure"].dt.day
    df["heure"] = df["date_heure"].dt.hour
    df["minute"] = df["date_heure"].dt.minute

    df["jour_semaine"] = df["date_heure"].dt.dayofweek
    df["nom_jour"] = df["date_heure"].dt.day_name()

    df["saison"] = df["mois"].map({
        12 : "Hiver",
        1 : "Hiver",
        2 : "Hiver",

        3 : "Printemps",
        4 : "Printemps",
        5 : "Printemps",

        6 : "été",
        7 : "été",
        8 : "été",

        9 : "Automne",
        10 : "Automne",
        11 : "Automne",
    })

    df["type_jour"] = df["jour_semaine"].map({lambda x : "Jour_de_semaine" if x < 5 else "Weekend"})

    return df
