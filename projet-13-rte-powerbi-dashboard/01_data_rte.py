import pandas as pd
import requests
import sqlite3

def recup_rte(debut_date="2024-01-01",fin_date="2026-01-01"):
    url = ("https://odre.opendatasoft.com"
        "/api/explore/v2.1/catalog/datasets"
        "/consommation-quotidienne-brute/records")

    limit = 100
    offset = 0
    tous_les_resultats = []

    while True:
        params = {
            "where" : (
                 f"date_heure >= '{debut_date}T00:00:00+01:00'"
                f" AND date_heure <= '{fin_date}T23:59:59+01:00'"
    ),
            "limit" : limit,
            "order_by" : "date_heure ASC",
            "select" : (
                "date_heure,"
                "consommation_brute_totale,"
                "consommation_brute_gaz_totale"
            ),
            "timezone" : "Europe/Paris",
            "offset" : offset,
        }
        reponse = requests.get(url,params=params)

        if reponse.status_code != 200:
            print(f"Erreur : {reponse.status_code}")
            print("fallback : Récupérons sur Eco2mix")
            return recup_eco2mix(debut_date, fin_date)

        data = reponse.json()
        resultats = data["results"]
        tous_les_resultats.extend(resultats)
        print(f"page offset={offset} : {len(resultats)} lignes récupérées")

        if len(resultats) < limit:
            break
        offset += limit

    df = pd.DataFrame(tous_les_resultats)
    print(f"le nombre de lignes RTE récupérées au total est {len(df)}")
    return df

def recup_eco2mix(debut_date="2024-01-01",fin_date="2024-10-01"):
    url = ("https://odre.opendatasoft.com"
        "/api/explore/v2.1/catalog/datasets"
        "/eco2mix-national-cons-def/records")

    params = {
        "where" : (
             f"date_heure >= '{debut_date}T00:00:00+01:00'"
            f" AND date_heure <= '{fin_date}T23:59:59+01:00'"
),
        "order_by" : "date_heure ASC",
        "timezone" : "Europe/Paris",
        "limit" : 100,
        "offset" : 0,
        "select" : (
            "date_heure,"
            "consommation,"
            "fioul,"
            "solaire,"
            "gaz"
        )
    }
    reponse = requests.get(url,params=params)
    if reponse.status_code == 200:
        print("Récupération de données réussis")
        data = reponse.json()
        df = pd.DataFrame(data["results"])
        print(f"le nombre de lignes récupérées est {len(df)}")
        return df
    else:
        print(f"Erreur : {reponse.status_code}")
        print("Accès impossible à Eco2mix")
        return None


df_rte = recup_rte()

if df_rte is None:
    print("Aucune donnée récupérée (RTE et Eco2mix ont échoué). Arrêt du script.")
    raise SystemExit(1)


connect = sqlite3.connect("data_reelle.db")
df_rte.to_sql(
    "eco_mix",
    connect,
    if_exists="replace",
    index=False
)
connect.close()

df_rte.to_csv(
    "data_eco2mix.csv",
    index=False
)

df = pd.read_csv("data_eco2mix.csv")

print(f"Colonnes : {df.columns.tolist()} ")
print(f"Nombre de valeurs manquantes : {df_rte.isnull().sum()}")


df = df.rename(columns={
    "date_heure" : "datetime",
    "consommation_brute_totale" : "conso_tot_mw",
    "consommation_brute_gaz_totale" : "conso_gaz_mw"
})

df["datetime"] = pd.to_datetime(df["datetime"], utc=True).dt.tz_convert("Europe/Paris")
df["date"] = df["datetime"].dt.date
df["heure"] = df["datetime"].dt.hour
df["mois"] = df["datetime"].dt.month
df["jour_semaine"] = df["datetime"].dt.dayofweek

def saison(mois):
    if mois in [12,1,2]:
        return "hiver"
    elif mois in [3,4,5]: 
        return "printemps"
    elif mois in [6,7,8]: 
        return "été"
    else:
        return "automne"

df["saison"] = df["mois"].apply(saison)


df.to_csv("rte_powerbi_ready.csv",index=False,encoding="utf-8-sig")
print(df.head())

