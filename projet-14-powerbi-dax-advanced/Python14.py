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

def renouvelable(df):
    for colonne in ["eolien","solaire","hydraulique"]:
        if colonne not in df.columns():
            df[colonne] = 0
        df[colonne] = pd.to_numeric(df[colonne], errors="coerce").fillna(0)

    df["renouvelable"] = (df["eolien"] + df["solaire"] + df["hydraulique"])

    if "consommation" in df.columns():
        df["consommation"] = pd.to_numeric(df["consommation"], errors="coerce")
        df["part_renouvel_%"] = (df["renouvelable"] / df["consommation"] *100).round(1)

    return df

def dataset(df):
    date_fin = datetime.now()
    date_debut = date_fin - timedelta(day=nb_jour)

    date_debut_str = date_debut.strftime("%Y-%m-%d %H:%M:%S")
    date_fin_str = date_fin.strftime("%Y-%m-%d %H:%M:%S")

    print(f"la date de début : {date_debut_str}")
    print(f"la date de fin : {date_fin_str}")

    df_natio = recup(url_regional,where)
    df_natio = temporalite(df)
    df_natio = renouvelable(df)
    df_natio = df.dropna(subset=["consommation"])
    df_region = recup(url_national,where)
    df_region = temporalite(df_region)
    df_region = renouvelable(df_region)
    
    connexion = sqlite3.connect("database.db")
    df_natio.to_sql("eco2mix_natio",connexion,if_exists="replace",index=False)
    df_region.to_sql("eco2mix_region",connexion,if_exists="replace",index=False)
    df_natio.to_csv("eco2mix_natio.csv", index=False,encoding="utf-8-sig")
    df_region.to_csv("eco2mix_region.csv", index=False,encoding="utf-8-sig")

    connexion.close()
    return df_natio,df_region


df, df_region = build_powerbi_dataset()





