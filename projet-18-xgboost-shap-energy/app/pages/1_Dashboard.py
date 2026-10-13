import sqlite3
from pathlib import Path 
import pandas as pd 
import plotly.express as px 
import streamlit as st 

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
    )

st.markdown("Exploration de la consommation électrique et des variables météo")

DATA_PATH = Path(__file__).resolve().parents[2] / "database" / "energy.db"

@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect(DATA_PATH)
    return pd.read_sql_query("SELECT * FROM v_ml_features ORDER BY datetime", conn)

try: 
    df = load_data()
    if df.empty: 
        st.warning("Aucune donnée disponible. Vérifie que la base SQLite est alimentée.")
        st.stop()
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["conso_mw","datetime"])
    if df.empty:
        st.warning("Aucune consommation exploitable dans la base")
        st.stop()
    st.sidebar.subheader("Filtres")
    date_debut = df["datetime"].min().date()
    date_fin = df["datetime"].max().date()
    periode = st.sidebar.date_input("Periode", value=(date_debut,date_fin))

    if isinstance(periode,(tuple,list)) and len(periode) == 2:
        date_debut,date_fin = periode
        df = df[(df["datetime"].dt.date >= date_debut) & (df["datetime"].dt.date <= date_fin)]
    if df.empty:
        st.warning("Auncune donnée pour cette période")
        st.stop()
    c1,c2,c3 = st.columns(3)
    c1.metric("Consommation moyenne en MW", f"{round(df["conso_mw"].mean(),0)} MW")
    c2.metric("Pic de consommation en MW", f"{round(df["conso_mw"].max(),0)} MW")
    c3.metric("Nombre d'observations",f"{round(len(df),0)}")

    st.subheader("Evolution de la consommation")
    fig = px.line(df, x="datetime",y="conso_mw", labels={
        "datetime" : "Date", "conso_mw" : "Consommation (MW)"
    } )
    st.plotly_chart(fig,width="stretch")

    if "temperature" in df.columns:
        st.subheader("Consommation et température")
        meteo_df = df.dropna(subset=["temperature"])
        if not meteo_df.empty:
            fig = px.scatter(meteo_df, x="temperature", y="conso_mw",trendline="ols",
                             labels= {
                                 "temperature" : "Température (°C)",
                                 "conso_mw" : "Consommation (MW)"
                             })
            st.plotly_chart(fig,width="stretch")

    with st.expander("Consulter les données"):
        st.dataframe(df, width="stretch")
except (sqlite3.Error, pd.errors.DatabaseError) as e:
    st.error(f"Erreur lors de la lecture de SQLite : {e}")



