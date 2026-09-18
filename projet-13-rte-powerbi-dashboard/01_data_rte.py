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





