import pandas as pd

def clean_consumption(df):
    if df is None or df.empty:
        return df
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["conso_mw"] = pd.to_numeric(df["conso_mw"], errors="coerce")
    df = df.dropna(subset=["datetime", "conso_mw"])
    df = df.drop_duplicates(subset=["datetime"])
    df = df.sort_values("datetime")
    return df.reset_index(drop=True)

def clean_generation(df):
    if df is None or df.empty:
        return df
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["production_mw"] = pd.to_numeric(df["production_mw"], errors="coerce")
    df["production_type"] = df["production_type"].astype("string").str.strip().str.upper()
    df = df.dropna(subset=["datetime", "production_mw", "production_type"])
    df = df.drop_duplicates(subset=["datetime", "production_type"])
    df = df.sort_values(["datetime", "production_type"])
    return df.reset_index(drop=True)

def clean_prices(df):
    if df is None or df.empty:
        return df
    df = df.copy()
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
    df["price_eur_mwh"] = pd.to_numeric(df["price_eur_mwh"], errors="coerce")
    df = df.dropna(subset=["datetime", "price_eur_mwh"])
    df = df.drop_duplicates(subset=["datetime"])
    df = df.sort_values("datetime")
    return df.reset_index(drop=True)

if __name__ == "__main__":

    exemple = pd.DataFrame({
        "datetime": [
            "2026-10-01T00:00:00Z",
            "2026-10-01T00:00:00Z",
            "2026-10-01T01:00:00Z",
        ],
        "conso_mw": [65000, 65000, None],
    })

    resultat = clean_consumption(exemple)

    print("Données nettoyées :")
    print(resultat)
