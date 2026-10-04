import requests
import pandas as pd

def clean_rte(df):
    df = df.copy()
    df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True).dt.tz_convert("Europe/Paris")
    colonnes_numériques = [
        "consommation",
        "nucleaire",
        "bioenergies",
        "eolien",
        "solaire",
    ]
    for colonne in colonnes_numériques:
        if colonne in df.columns:
            df[colonne] = pd.to_numeric(df[colonne], errors="coerce")
    df = df.dropna(subset="consommation")
    df["heure"] = df["date_heure"].dt.hour
    df["jour_semaine"] = df["date_heure"].dt.dayofweek
    df["type_jour"] = df["jour_semaine"].apply(lambda x : "Semaine" if x < 5 else "Weekend")
    df["mois"] = df["date_heure"].dt.month

    def saison(mois):
        if mois in [12,1,2]:
            return "Hiver"
        elif mois in [3,4,5]:
            return "Printemps"
        elif mois in [6,7,8]:
            return "Ete"
        else:
            return "Automne"

    df["saison"] = df["mois"].apply(saison)
    return df

def clean_meteo(df): 
    df = df.copy()
    df["time"] = pd.to_datetime(df["time"])
    df["temperature_2m"] = pd.to_numeric(df["temperature_2m"], errors="coerce")
    df["precipitation"] = pd.to_numeric(df["precipitation"], errors="coerce")
    df = df.dropna(subset=["time","ville"])
    df = df.drop_duplicates(subset=["time","ville"])
    df = df.sort_values(["time","ville"])
    return df

if __name__ == "__main__":
    print("Module de nettoyage prêt.")


    
