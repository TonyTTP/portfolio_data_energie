from pathlib import Path
import sqlite3
import pandas as pd
from fetch_data import fetch_data
from train import train_models

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "energy.db"
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def diagnose(results, model_name="xgboost"):
    result = results[model_name]
    diagnostics = pd.DataFrame({
        "conso_reelle_mw": result["y_test"].to_numpy(),
        "conso_predite_mw": result["predictions"]
    })

    diagnostics["ecart_mw"] = (
        diagnostics["conso_predite_mw"]
        - diagnostics["conso_reelle_mw"]
    )

    diagnostics["ecart_pct"] = (
        diagnostics["ecart_mw"]
        / diagnostics["conso_reelle_mw"].replace(0, float("nan"))
        * 100
    )

    diagnostics["erreur_absolue_mw"] = (
        diagnostics["ecart_mw"].abs()
    )

    seuil = diagnostics["erreur_absolue_mw"].quantile(0.95)

    diagnostics["anomalie"] = (
        diagnostics["erreur_absolue_mw"] > seuil
    )

    diagnostics["diagnostic"] = diagnostics.apply(
        lambda row: (
            "Sous-estimation du modèle"
            if row["ecart_mw"] < 0
            else "Surestimation du modèle"
        ),
        axis=1
    )

    return diagnostics.sort_values(
        "erreur_absolue_mw",
        ascending=False
    )


def save_diagnostics(df):
    df.to_csv(
        OUTPUT_DIR / "diagnostics.csv",
        index=False
    )

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            "xgboost_diagnostics",
            conn,
            if_exists="replace",
            index=False
        )

    print("Diagnostics enregistrés dans SQLite et outputs/.")


if __name__ == "__main__":
    results = train_models()
    diagnostics = diagnose(results)
    save_diagnostics(diagnostics)

    print(diagnostics.head(10).to_string(index=False))
