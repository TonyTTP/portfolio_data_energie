from datetime import datetime, timedelta
import requests 
import pandas as pd

def fetch_eco2mix(days_back=90):
    fin = datetime.now()
    debut = datetime.now() - timedelta(days_back)
    url = (        "https://odre.opendatasoft.com"
        "/api/explore/v2.1/catalog/datasets"
        "/eco2mix-national-tr/records")
    params = {
            "where": (f"date_heure >= '{debut:%Y-%m-%d}'"
            f" AND date_heure <= '{fin:%Y-%m-%d}T23:59:59'"
            " AND consommation IS NOT NULL"),
            "limit" : 100,
            "order_by" : "date_heure ASC",
            "select" : ",".join([
                "consommation",
                "solaire",
                "eolien",
                "hydraulique",
                "nucleaire",
                "date_heure",
                "bioenergies",
                "taux_co2"]),
            "timezone" : "Europe/Paris"
    }

    try:
        resultats = []
        offset = 0
        while True:
            params["offset"] = offset
            reponse = requests.get(url, params=params, timeout=10)
            reponse.raise_for_status()
            page = reponse.json()["results"]
            if not page:
                break
            resultats.extend(page)
            offset += 100
        df = pd.DataFrame(resultats)
        df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True).dt.tz_convert("Europe/Paris")
        return df
    except Exception as e:
        print(f"L'erreur : {e}")
        return None
    
if __name__ == "__main__" :
    df_rte = fetch_eco2mix(days_back=90)
    if df_rte is not None:
        print(df_rte.head())
        print(df_rte.shape)

