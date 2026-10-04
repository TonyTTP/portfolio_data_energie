import requests 
import pandas as pd

def fetch_meteo(days_back=90):
    villes = {"Paris" : (48.86,2.26),"Lyon" : (45.75,4.79),"Marseille" : (43.28,5.29)}
    dfs = []
    for ville,(lat,long) in villes.items():
        url = "https://api.open-meteo.com/v1/forecast"
        params = {

            "latitude" : lat,
            "longitude" : long,
            "timezone" : "Europe/Paris",
            "hourly" : "temperature_2m,precipitation",
            "past_days" : days_back,
            "forecast_days" : 7
        }
        try:
            reponse = requests.get(url,params=params,timeout=10)
            reponse.raise_for_status()
            df = pd.DataFrame(reponse.json()["hourly"])
            df["time"] = pd.to_datetime(df["time"])
            df["ville"] = ville
            dfs.append(df)
        except Exception as e:
            print(f"Erreur : {e}")
    if not dfs:
        return None
    return pd.concat(dfs, ignore_index=True)

if __name__ == "__main__":
    df_meteo = fetch_meteo(days_back=30)
    if df_meteo is not None:
        print(df_meteo.head())
        print(df_meteo.shape)


        