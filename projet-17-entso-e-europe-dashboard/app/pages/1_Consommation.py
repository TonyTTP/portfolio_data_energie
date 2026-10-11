import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard Consommation électrique",
    page_icon="⚡",
    layout="wide"
)

st.title("Consommation électrique européenne")
st.caption("Analyse de la demande électrique par pays")

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "database" / "energy_oauth.db"

@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query("SELECT * FROM entsoe_load",conn)

try:
    df = load_data()
except Exception as error:
    st.error(f"Erreur de chargement : {error}")
    st.stop()

df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
df["conso_mw"] = pd.to_numeric(df["conso_mw"], errors="coerce")

df = df.dropna(subset=["datetime","conso_mw"])

st.sidebar.header("Filtres")

countries = sorted(df["country_name"].dropna().unique())

selected_countries = st.sidebar.multiselect("Pays",options=countries,default=countries[:3])

df = df[df["country_name"].isin(selected_countries)]

if df.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

c1,c2,c3 = st.columns(3)

c1.metric("Consommation moyenne", f"{df['conso_mw'].mean():,.0f} MW")
c2.metric("Consommation maximale", f"{df['conso_mw'].max():,.0f} MW")
c3.metric("Nombre de pays", df["country_name"].nunique())

st.subheader("Évolution de la demande électrique")

fig = px.line(df.sort_values("datetime"), x="datetime", y="conso_mw", color="country_name",
              title="Évolution de la consommation en fonction du temps",
              labels={
                  "datetime" : "Date et heure",
                  "conso_mw" : "Consommation (MW)",
                  "country_name" : "Pays"
              })

st.plotly_chart(fig, width="stretch")

st.subheader("Consommation moyenne par pays")

comparaison = (df.groupby("country_name", as_index=False)["conso_mw"].mean().sort_values("conso_mw", ascending=True))

fig = px.bar(comparaison, x="conso_mw", y="country_name", orientation="h",
             labels= {
                 "conso_mw" : "Consommation moyenne (MW)",
                 "country_name" : "Pays"
             })
st.plotly_chart(fig, width="stretch")

with st.expander("Afficher les données détaillées"):
    st.dataframe(df, width="stretch")
