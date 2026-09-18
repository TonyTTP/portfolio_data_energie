import pandas as pd
import request 
import sqlite3 

def recup_rte(debut_date="2024-01-01",fin_date="2024-10-01"):
    url = ("https://data.rte-france.com"
        "/api/explore/v2.1/catalog/datasets"
        "/consommation-quotidienne-brute/records")

    params = {
        "where" : (
             f"date_heure >= '{debut_date}T00:00:00+01:00'"
            f" AND date_heure <= '{fin_date}T23:59:59+01:00'"
),
        "limit" : 100,
        "order_by" : "date_heure ASC",
        "select" : (
            "date_heure,"
            "consommation_brute_total,"
            "consommation_brute_gaz,"
            "consommation_brute_fioul,"
        ),
        "timezone" : "Europe/Paris", 
        "offset" : 0,
    }
    reponse = resquests.get(url,params=params)

    if reponse.status_code == 200:
        data = reponse.json()
        print("Récuperation valide")
        df = pd.DataFrame(data["results"])
        print(f"le nombre de lignes RTE récupérées est {len(df)}")
        return df

    else: 
        print(f"Erreur : {reponse.status_code}")
        print("fallback : Récupérons sur Eco2mix")

        return recup_eco2mix()

def recup_eco2mix(debut_date="2024-01-01",fin_date="2024-10-01"):
    url = ("https://data.rte-france.com"
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
        "select" : {
            "date_heure"
            "consommation",
            "fioul",
            "solaire",
            "gaz",

        }
    }
    reponse = requests.get(url,params=params)
    if reponse.status_code() == 200:
        print("Récupération de données réussis")
        data = reponse.json()
        df = pd.DataFrame(data["results"])
        print(f"le nombre de lignes récupérées est {len(df)}")
        return df
    else:
        print("Accès impossible à Eco2mix")


df_rte = recup_eco2mix()


connect = sqlite3.connect("data_reelle")
df_rte.to_sql(
    "eco_mix",
    connect,
    if_exists="replace",
    index=False
)

df_rte.to_csv(
    "data_eco2mix.csv",
    index=False
)

df = pd.read_csv("data_eco2mix.csv")

print(f"Colonnes : {df.columns.tolist()} ")
print(f"Nombre de valeurs manquantes : {df_rte.isnull().sum()}")


df = df.rename(columns={
    "date_heure" : "datetime",
    "consommation_brute_total" : "conso_tot_mw",
    "consommation_brute_gaz" : "conso_gaz_mw",
    "consommation_brute_fioul" : "conso_fioul_mw"
})

df["datetime"] = pd.to_datetime(df["datetime"])
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


df.to_csv("rte_powerbi_ready",index=False,encoding="utf-8-sig")
print(df.head)

