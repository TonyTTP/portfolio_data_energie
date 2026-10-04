import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "data"))

import numpy as np
from fetch_rte import fetch_eco2mix
from clean import clean_rte

def anomaly(df,seuil_z=2):
    df = df.copy()
    moyenne = df["consommation"].mean()
    ecartype = df["consommation"].std()
    df["z_score"] = (df["consommation"] - moyenne) / ecartype
    df["anomalie"] = np.abs(df["z_score"]) >= seuil_z
    df["type_anomalie"] = np.where(df["z_score"]  >= seuil_z,"pic_haut",
                             np.where(df["z_score"]  <= -seuil_z,"pic_bas","normal"))
    compteur_anomalie = sum(df["anomalie"])
    print(f"Nombre d'anomalie : {compteur_anomalie}")
    return df

if __name__ == "__main__":
    df_rte = fetch_eco2mix(days_back=90)
    if df_rte is not None:
        df_anomalies = anomaly(clean_rte(df_rte))
        print(df_anomalies["type_anomalie"].value_counts())