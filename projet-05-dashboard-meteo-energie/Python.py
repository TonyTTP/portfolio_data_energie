import requests
import pandas as pd
import sqlite3
import numpy as np
import matplotlib.pyplot as plt

# On va utiliser une API publique gratuite
# API Open-Meteo 
# Documentation : https://open-meteo.com , https://open-meteo.com/en/docs

url = "https://api.open-meteo.com/v1/forecast"

params = { 
    "latitude"  : 48.85,   
    "longitude" : 2.35,
    "daily"     : "temperature_2m_max", 
    "timezone"  : "Europe/Paris",
    "past_days" : 7 
}


response = requests.get(url, params=params)

if response.status_code == 200:


    data = response.json()


    print("Clés du JSON :")
    print(data.keys())

else:
    print("Erreur lors de la requête.")
    print(response.text)




if response.status_code == 200:

    data = response.json()



    dates = data["daily"]["time"]
    temp_max = data["daily"]["temperature_2m_max"]


    df = pd.DataFrame({
        "date": dates,
        "temp_max": temp_max
    })


    df["date"] = pd.to_datetime(df["date"])


    plus_chaud = df.loc[df["temp_max"].idxmax()]

    print("Jour le plus chaud :")
    print(plus_chaud)

else:
    print("Erreur :", response.status_code)



url = "https://api.open-meteo.com/v1/forecast"


def recuperer_meteo(ville, lat, lon):

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max",
        "timezone": "Europe/Paris",
        "past_days": 30
    }

    response = requests.get(url, params=params)

    data = response.json()

    df = pd.DataFrame({
        "date": data["daily"]["time"],
        "temp_max": data["daily"]["temperature_2m_max"]
    })

    df["date"] = pd.to_datetime(df["date"])
    df["ville"] = ville

    return df


df_paris = recuperer_meteo(
    "Paris",
    48.85,
    2.35
)


df_lyon = recuperer_meteo(
    "Lyon",
    45.75,
    4.85
)





df_total = pd.concat(
    [df_paris, df_lyon],
    ignore_index=True
)


conn = sqlite3.connect("meteo_france.db")

df_total.to_sql(
    "temperatures",
    conn,
    if_exists="replace",
    index=False
)

requete = """
SELECT ville,
       AVG(temp_max) AS temp_moyenne
FROM temperatures
GROUP BY ville
ORDER BY temp_moyenne DESC
LIMIT 1
"""

resultat = pd.read_sql_query(
    requete,
    conn
)

print(resultat)

conn.close()



import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=90)


temperature = np.random.randint(-5, 25, 90)
conso = 800 - (temperature * 15) + np.random.normal(0, 50, 90)

df = pd.DataFrame({
    "date"    : dates,
    "temp_c"  : temperature,
    "conso_mw": conso
})



correlation = df["temp_c"].corr(df["conso_mw"])

print(correlation)


def saison(mois):

    if mois in [12, 1, 2]:
        return "hiver"

    elif mois in [3, 4, 5]:
        return "printemps"

    elif mois in [6, 7, 8]:
        return "été"

    else:
        return "automne"

df["saison"] = df["date"].dt.month.apply(saison)

print(df.head())


conso_saison = (
    df.groupby("saison")["conso_mw"].mean().sort_values(ascending=False)
)

print(conso_saison)

# Projet : Tableau de bord météo-énergie



url = "https://api.open-meteo.com/v1/forecast"

villes = {
    "Paris": (48.85, 2.35),
    "Lyon": (45.75, 4.85),
    "Marseille": (43.30, 5.40)
}

liste_df = []

for ville, (lat, lon) in villes.items():

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",
            "precipitation_sum"
        ],
        "timezone": "Europe/Paris",
        "past_days": 30
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:

        data = response.json()

        df = pd.DataFrame({
            "date": data["daily"]["time"],
            "temp_max": data["daily"]["temperature_2m_max"],
            "precipitation": data["daily"]["precipitation_sum"]
        })

        df["date"] = pd.to_datetime(df["date"])
        df["ville"] = ville

        liste_df.append(df)



df_total = pd.concat(
    liste_df,
    ignore_index=True
)

print(df_total.head())


conn = sqlite3.connect("dashboard_energie.db")

df_total.to_sql(
    "meteo_villes",
    conn,
    if_exists="replace",
    index=False
)



requete_froide = """WITH moyenne_mensuelle AS (
    SELECT strftime('%Y-%m', date) AS mois,ville, AVG(temp_max) AS temp_moyenne
    FROM meteo_villes
    GROUP BY mois, ville
)

SELECT *
FROM moyenne_mensuelle
ORDER BY mois, temp_moyenne ASC
"""

resultat_froid = pd.read_sql_query(
    requete_froide,
    conn
)

print("\nVille la plus froide par mois :")
print(resultat_froid)



requete_difficile = """
SELECT *
FROM meteo_villes
WHERE precipitation > 5
AND temp_max < 5
"""

jours_difficiles = pd.read_sql_query(
    requete_difficile,
    conn
)

print("\nJours difficiles :")
print(jours_difficiles)

conn.close()



fig, axes = plt.subplots(3,1,figsize=(12, 12))



for ville in df_total["ville"].unique():
    df_ville = df_total[df_total["ville"] == ville]
    axes[0].plot(df_ville["date"],df_ville["temp_max"],label=ville)

axes[0].set_title("Température maximale")
axes[0].set_ylabel("°C")
axes[0].legend()



for ville in df_total["ville"].unique():
    df_ville = df_total[df_total["ville"] == ville]
    axes[1].bar(df_ville["date"], df_ville["precipitation"], label=ville, alpha=1)

axes[1].set_title("Précipitations")
axes[1].set_ylabel("mm")
axes[1].legend()



axes[2].scatter(df_total["temp_max"], df_total["precipitation"], alpha=0.5)


z = np.polyfit(df_total["temp_max"], df_total["precipitation"], 1)
p = np.poly1d(z)
x_line = np.linspace(df_total["temp_max"].min(), df_total["temp_max"].max(), 100)
axes[2].plot(x_line, p(x_line), color="red", label="tendance")

axes[2].set_title("Corrélation Température vs Précipitations")
axes[2].set_xlabel("Température max (°C)")
axes[2].set_ylabel("Précipitations (mm)")
axes[2].legend()


plt.tight_layout()
plt.show()



