import numpy as np 
import pandas as pd 
from fetch_data import fetch_data
from clean import clean_data

def build_features(df): 
    df = df.copy()
    if "datetime" in df.columns:
        dt = pd.to_datetime(df["datetime"])
        df["heure"] = dt.dt.hour
        df["mois"] = dt.dt.month
        df["jour_semaine"] = dt.dt.dayofweek

        if "heure" in df.columns:
            df["heure_sin"] = np.sin(2*np.pi*df["heure"]/24)
            df["heure_cos"] = np.cos(2*np.pi*df["heure"]/24)
        if "mois" in df.columns:
            df["mois_sin"] = np.sin(2*np.pi*(df["mois"] - 1)/12)
            df["mois_cos"] = np.cos(2*np.pi*(df["mois"] - 1)/12)
        df["est_hiver"] = df["mois"].isin([12,1,2]).astype(int)
        if "jour_semaine" in df.columns: 
            df["est_weekend"] = df["jour_semaine"].isin([5,6]).astype(int)
        if "datetime" in df.columns:
            df = df.sort_values("datetime")
            if "conso_lag_48h" not in df.columns:
                df["conso_lag_48h"] = df["conso_mw"].shift(48)
            if "conso_lag_7j" not in df.columns:
                df["conso_lag_7j"] = df["conso_mw"].shift(168)
            if "conso_rolling_48h" not in df.columns:
                df["conso_rolling_48h"] = df["conso_mw"].shift(1).rolling(48).mean()
    return df.reset_index(drop=True)

if __name__ == "__main__":
    df = build_features(clean_data(fetch_data()))
    print(df.head(5))
    print(df.columns.tolist())
    
