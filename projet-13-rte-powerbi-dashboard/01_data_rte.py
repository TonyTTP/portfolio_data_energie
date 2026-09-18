import pandas as pd
import request 
import sqlite3 

def recup_rte(debut_date,fin_date):
    url = ("https://data.rte-france.com"
        "/api/explore/v2.1/catalog/datasets"
        "/consommation-quotidienne-brute/records")

    params = {
        "where" : "date_heure" > debut_date & "date_heure" < fin_date,
        "limit" : 100,
        "order by" : "date_heure ASC",
        "select" : (
            "date_heure,"
            "consommation_brute_total,"
            "consommation_brute_gaz,"
            "consommation_brute_fioul,"
        ),
        "time_zone" : "Europe/Paris", 
        "offset" : 0,
    }
    reponse = resquest.get(url,params=params)

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

def recup_eco2mix(debut_date,fin_date):

