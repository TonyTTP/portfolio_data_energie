import sqlite3 
from pathlib import Path 
import joblib 
import pandas as pd 

ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_DIR / "models" / "saved" / "xgb_energy_model.joblib"
FEATURES = ("heure_sin", "heure_cos", "mois_sin", "mois_cos", "est_weekend", "est_hiver", "conso_lag_48h","conso_lag_7j")

def predict_consumption(data):
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Modèle introuvable, lance d'abord train")
    missing = set(FEATURES) - set(data.columns)
    if missing:
        raise ValueError(f"Variables manquantes : {sorted(missing)}")
    model = joblib.load(MODEL_PATH)
    X = data[list(FEATURES)]
    predictions = model.predict(X)
    return predictions

if __name__ == "__main__":
    DB_PATH = ROOT_DIR / "database" / "energy.db"
    conn = sqlite3.connect(DB_PATH)
    sample = pd.read_sql_query(
            """
            SELECT heure_sin, heure_cos,
                   mois_sin, mois_cos,
                   est_weekend, est_hiver,
                   conso_lag_48h, conso_lag_7j
            FROM eco2mix
            WHERE conso_lag_48h IS NOT NULL
              AND conso_lag_7j IS NOT NULL
            ORDER BY date_heure DESC
            LIMIT 1
            """,
            conn,
        )
    if sample.empty:
        raise ValueError("Aucune observation exploitable sur SQLite")
    predictions = predict_consumption(sample)
    print(f"Consommation prédite {predictions[0]:.2f} MW")
    