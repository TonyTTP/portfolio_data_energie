import pandas as pd
import numpy as np 
from fetch_rte import fetch_eco2mix

def clean_and_features(df):
    df = df.copy()
    df = df.drop_duplicates("date_heure")
    cols_numeriques = (
        "consommation","nucleaire","eolien","solaire","hydraulique","bioenergies"
    )
    for col in cols_numeriques:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].interpolate())
    df = df.dropna(subset="consommation")
    df["heure"] = df["date_heure"].dt.hour
    df["mois"] = df["date_heure"].dt.month
    df["jour_semaine"] = df["date_heure"].dt.dayofweek
    df["est_hiver"] = df["mois"].isin([12,1,2]).astype(int)
    df["est_weekend"] = df["jour_semaine"].isin([5,6]).astype(int)
    df["heure_sin"] = np.sin(2*np.pi*df["heure"]/24)
    df["heure_cos"] = np.cos(2*np.pi*df["heure"]/24)
    df["mois_sin"] = np.sin(2*np.pi*df["mois"]/12)
    df["mois_cos"] = np.cos(2*np.pi*df["mois"]/12)   

    df["conso_lag_48h"] = df["consommation"].shift(48)
    df["conso_lag_7j"] = df["consommation"].shift(336)
    df["conso_rolling_48h"] = df["consommation"].rolling(48,min_periods=1).mean()

    df["renouvelable"] = df["eolien"] + df["solaire"] + df["hydraulique"]

    df["part_ener_%"] = round(df["renouvelable"]/df["consommation"]*100,1)
    print(f"Nombre de colonnes est {len(df.columns)}")
    print(f"Nombre de lignes est {len(df)}")
    return df


if __name__ == "__main__":
    df_raw   = fetch_eco2mix(days_back=30)
    df_clean = clean_and_features(df_raw)
    print(df_clean[["date_heure", "consommation","heure_sin", "conso_lag_48h"]].head())


