from pathlib import Path 
import sqlite3 
import pandas as pd 


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "energy.db"

def fetch_data():
    if not DB_PATH.exists():
        raise FileNotFoundError("Le fichier n'a pas été trouvé")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM v_ml_features", conn)
    if df.empty:
        raise ValueError("Aucune donnée disponible")
    print(f"{len(df)} lignes récupérées")
    return df

if __name__ == "__main__":
    df = fetch_data()
    print(df.head(5))
    print(df.info())