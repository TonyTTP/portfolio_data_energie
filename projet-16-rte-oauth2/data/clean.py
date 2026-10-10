#fonction consumption # si df est rien ou vide alor df
#copie datetime conso_mw supprimer les na supprimer les doublons retourner

#generation pareil mais avec datetime production_mw production_type...

#exchanges pareil datetime, flow_mw, sender = convertit en text enleve espace et met en majuscule receiver

import pandas as pd


def clean_consumption(df):
    if df is None or df.empty:
        return df
    df = df.copy()

    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df["conso_mw"] = pd.to_numeric(df["conso_mw"], errors="coerce")
    df = df.dropna(subset=["datetime", "conso_mw"])
    df = df.drop_duplicates()

    return df


def clean_generation(df):
    if df is None or df.empty:
        return df
    df = df.copy()

    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df["production_mw"] = pd.to_numeric(df["production_mw"], errors="coerce")
    df["production_type"] = df["production_type"].astype(str).str.strip().str.upper()  # du texte, pas un nombre
    df = df.dropna(subset=["datetime", "production_mw", "production_type"])
    df = df.drop_duplicates()

    return df


def clean_exchanges(df):
    if df is None or df.empty:
        return df
    df = df.copy()

    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
    df["flow_mw"] = pd.to_numeric(df["flow_mw"], errors="coerce")
    df["sender"] = df["sender"].astype(str).str.strip().str.upper()
    df["receiver"] = df["receiver"].astype(str).str.strip().str.upper()
    df["direction"] = df.apply(
        lambda row: "import" if row["receiver"] == "FRANCE"
        else "export" if row["sender"] == "FRANCE"
        else "other",
        axis=1,
    )
    df = df.dropna(subset=["datetime", "flow_mw", "sender", "receiver"])
    df = df.drop_duplicates()

    return df
