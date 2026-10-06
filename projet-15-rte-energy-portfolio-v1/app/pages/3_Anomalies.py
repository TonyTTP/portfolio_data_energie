import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from models.anomaly import anomaly

DATABASE = "database.db"

st.title("Détection des anomalies")

@st.cache_data(ttl=1800)
def load_data():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql(
        """ SELECT date_heure, consommation, saison
        FROM eco2mix
        WHERE consommation IS NOT NULL
        ORDER BY date_heure""",
        conn
    )
    conn.close()

    df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True).dt.tz_convert("Europe/Paris")
    return df

df = load_data()

seuil_z = st.slider("Seuil du z-score", min_value=1.0, max_value=4.0, value=2.0, step=0.5)

if st.button("Détecter les anomalies"):
    with st.spinner("Chargement..."):
        df_anomalies = anomaly(df,seuil_z=seuil_z)
    st.success("Détection terminée")

    nb_anomalies = int(df_anomalies["anomalie"].sum())

    taux_anomalies = (nb_anomalies/ len(df_anomalies)* 100)

    c1,c2 = st.columns(2)

    c1.metric("Nombre d'anomalies", nb_anomalies)
    c2.metric("Taux d'anomalie", f"{taux_anomalies:.2f} %")

    fig = px.scatter(df_anomalies, x="date_heure", y="consommation", color="type_anomalie",title="Anomalies de consommation",        labels={
            "date_heure": "Date",
            "consommation": "Consommation (MW)",
            "type_anomalie": "Type"
        },)

    st.plotly_chart(fig, width="stretch")

    st.header("Détail des anomalies")
    anomalies = df_anomalies[df_anomalies["anomalie"]].copy()

    st.dataframe(anomalies[["date_heure","consommation","z_score","type_anomalie","saison"]], width="stretch")
