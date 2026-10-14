import sqlite3 
from pathlib import Path 
import sys 
import pandas as pd 
import plotly.express as px 
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT_DIR / "models"))
from predict import predict_consumption, FEATURES

DB_PATH = ROOT_DIR / "database" / "energy.db"

st.title("📈 Prévisions énergétiques")
st.caption("Modèle XGBoost entraîné sur les données RTE")
if not DB_PATH.exists():
    st.warning("Base de données introuvable")
    st.stop()

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query(""" 
    SELECT date_heure, consommation,
            heure_sin, heure_cos,
            mois_sin, mois_cos,
            est_weekend, est_hiver,
            conso_lag_48h, conso_lag_7j
    FROM eco2mix
    ORDER BY date_heure""",conn)

df["date_heure"] = pd.to_datetime(df["date_heure"])
df = df.dropna(subset=["consommation"]+list(FEATURES))

if df.empty:
    st.warning("Aucune données")
    st.stop()

if st.button("Calculer les prédictions"):
    with st.spinner("Chargement"):
        try:
            df["prediction"] = predict_consumption(df[list(FEATURES)])
            fig = px.line(df.tail(500),title="Consommation réelle et prédite", x="date_heure",y=["consommation","prediction"],
                                        labels={
                                            "date_heure" : "Date",
                                            "consommation" : "Consommation (MW)"
                                        })
            st.plotly_chart(fig,width="stretch")
            st.dataframe(
            df[["date_heure", "consommation", "prediction"]].tail(50),
            width="stretch",
        )

        except FileNotFoundError:
            st.error("Entraîne d'abord le modèle avec models/train.py.")

        except Exception as e:
            st.error(f"Erreur lors de la prédiction : {e}")