import pandas as pd 
from fetch_data import fetch_data
def clean_data(df):
    df = df.copy()
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df = df.dropna(subset="datetime")
        df = df.sort_values("datetime")
    df = df.drop_duplicates()

    numeric_columns = ["temperature","precipitation","irradiation",
                       "conso_lag_48h","conso_lag_7j","conso_rolling_48h", "conso_mw"]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col],errors="coerce")
    df = df.dropna(subset=["conso_mw"])
    df = df[df["conso_mw"] >= 0]
    return df.reset_index(drop=True)

if __name__ == "__main__":
    df = clean_data(fetch_data())
    print(df.isna().sum())
    

    
