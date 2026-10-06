import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

import sqlite3
import streamlit as st
import pandas as pd
from models.forecast import train
import plotly.graph_objects as go

DATABASE = "database.db"

st.title("Prévisions de consommation")

@st.cache_data(ttl=1800)
def load_data():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql("""
    SELECT date_heure, consommation FROM eco2mix
    WHERE consommation IS NOT NULL
    ORDER BY date_heure """,
    conn)
    conn.close()
    df["date_heure"] = pd.to_datetime(df["date_heure"], utc=True).dt.tz_convert("Europe/Paris")
    return df

df = load_data()

st.write(
    "Prévision de la consommation électrique "
    "à partir des données historiques RTE."
)

heures = st.slider(
        "Nombre d'heures à prévoir", min_value=24, max_value=240,value=48,step=24)

if st.button("Lancer la prévision"):
    with st.spinner("Chargement..."):
        rmse, mape, forecast, model = train(df,periods=heures*4)
    st.success("Prévision terminée")

    c1,c2 = st.columns(2)
    c1.metric("MAPE", f"{mape:.2f} %" if mape is not None else "N/A")
    c2.metric("RMSE", f"{rmse:.2f} MW" if rmse is not None else "N/A")

    debut = df["date_heure"].max().tz_localize(None) - pd.Timedelta(days=7)
    historique = df[df["date_heure"].dt.tz_localize(None) >= debut]
    prevision = forecast[forecast["ds"] >= debut]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=historique["date_heure"].dt.tz_localize(None),
        y=historique["consommation"],
        mode="lines",
        name="Courbe de consommation"
    ))

    fig.add_trace(go.Scatter(
        x=prevision["ds"],
        y=prevision["yhat"],
        mode="lines",
        name="Prévision"
    ))

    fig.add_trace(go.Scatter(
        x=prevision["ds"],
        y=prevision["yhat_lower"],
        mode="lines",
        name="Borne inférieure de la prévision"

    ))

    fig.add_trace(go.Scatter(
        x=prevision["ds"],
        y=prevision["yhat_upper"],
        mode="lines",
        name="Borne supérieure de la prévision"

    ))

    fig.update_layout(
        title="Prévision de la consommation électrique",
        xaxis_title="Date",
        yaxis_title="Consommation (MW)",

    )

    st.plotly_chart(fig, width="stretch")
