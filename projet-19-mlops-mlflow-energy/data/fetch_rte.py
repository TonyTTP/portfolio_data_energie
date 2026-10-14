import requests 
import pandas as pd 
from datetime import datetime, timedelta 

def fetch_eco2mix(days_back=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)
    url = ("https://odre.opendatasoft.com""/api/explore/v2.1/catalog/datasets""/eco2mix-national-tr/exports/json")
    params = {
        "where" : (f"date_heure >= "f"'{start_date:%Y-%m-%d}T00:00:00'"
            f" AND date_heure <= "f"'{end_date:%Y-%m-%d}T23:59:59'"
            " AND consommation IS NOT NULL"),
        "order_by" : "date_heure ASC",
        "select" : ("date_heure,""consommation,""nucleaire,""eolien,"
        "solaire,""hydraulique," "bioenergies,""taux_co2"),
        "timezone" : "Europe/Paris"
    }
    try: 
        r = requests.get(url,params=params,timeout=10)
        r.raise_for_status()
        rep = r.json()
        df = pd.DataFrame(rep)
        df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True).dt.tz_convert("Europe/Paris")
        print(f"{len(df)} lignes récupérées")
        print(df.info())
        return df 
    except Exception as e:
        print(f"Erreur fetch RTE : {e}")
        return None

if __name__ == "__main__":
    df = fetch_eco2mix(days_back=30)
    if df is not None:
        print(df.head(5))
        print(f"Colonnes : {df.columns.tolist()}")

