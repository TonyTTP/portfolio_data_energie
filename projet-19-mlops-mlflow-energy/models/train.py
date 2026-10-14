import sqlite3
from pathlib import Path 
import joblib 
import pandas as pd 
import xgboost as xgb 

ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "database" / "energy.db"
MODEL_DIR = ROOT_DIR / "models" / "saved"
MODEL_PATH = MODEL_DIR / "xgb_energy_model.joblib"

FEATURES = ("heure_sin","heure_cos", "mois_sin", "mois_cos","est_weekend","est_hiver",
            "conso_lag_48h", "conso_lag_7j")

TARGET = "consommation"

def load_data(): 
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * from eco2mix ORDER BY date_heure",conn)
    df["date_heure"] = pd.to_datetime(df["date_heure"])
    return df 

def train_model():
    df = load_data()
    df = df.dropna(subset=list(FEATURES) + ["consommation"])
    df = df.copy() 
    if len(df) < 50:
        raise ValueError(f"le nombre de lignes est {len(df)},récupère davantage de données")
    X = df[list(FEATURES)]
    y = df["consommation"]
    split = int(len(df)*0.8) 
    X_train = X.iloc[:split]
    y_train = y.iloc[:split]
    X_test = X.iloc[split:]
    y_test = y.iloc[split:]
    model = xgb.XGBRegressor(n_estimators=300,learning_rate=0.05,max_depth=6,
                             subsample=0.8,
                            objective="reg:squarederror",random_state=42, n_jobs=-1,)

    model.fit(X_train,y_train)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Lignes d'entraînement : {len(X_train)}")
    print(f"Lignes de test : {len(X_test)}")
    print(f"Modèle sauvegardé : {MODEL_PATH}")
    return model, X_test, y_test

if __name__ == "__main__":
    train_model()




