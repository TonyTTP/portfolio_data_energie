import sqlite3
import plotly.express as px
import pandas as pd
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="Mix énergétique",
    page_icon="🌱",
    layout="wide"
)

st.title("Mix énergétique européen")

st.caption("Analyse de la production électrique par source d'énergie")

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "database" / "energy_oauth.db"

@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query("SELECT * FROM entsoe_generation", conn)

try:
    df = load_data()
except Exception as error:
    st.error(f"Erreur de chargement : {error}")
    st.stop()

df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")
df["production_mw"] = pd.to_numeric(df["production_mw"], errors="coerce")
df = df.dropna(subset=["datetime", "production_mw", "production_type"])

st.sidebar.header("Filtres")

countries = sorted(df["country_name"].dropna().unique())
selected_countries = st.sidebar.multiselect("Pays", options=countries,default=countries[:3])

energie = sorted(df["production_type"].dropna().unique())

selected_energy = st.sidebar.multiselect("Énergie",options=energie, default=energie[:2])

df = df[df["country_name"].isin(selected_countries) & df["production_type"].isin(selected_energy)]

if df.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

c1,c2,c3 = st.columns(3)

c1.metric("Puissance moyenne", f"{df['production_mw'].mean():,.0f} MW")
c2.metric("Puissance maximale", f"{df['production_mw'].max():,.0f} MW")
c3.metric("Nombre de sources différentes", df["production_type"].nunique())

st.subheader("Répartition de la production par source")

production_moy = df.groupby("production_type",as_index=False)["production_mw"].mean()

fig_pie = px.pie(production_moy, names="production_type", values="production_mw")

st.plotly_chart(fig_pie, width="stretch")

st.subheader("Évolution de la production dans le temps")

production_time = df.groupby(["datetime", "country_name", "production_type"], as_index=False)["production_mw"].sum()

fig = px.line(production_time.sort_values("datetime"), x="datetime", y="production_mw", color="production_type", line_dash="country_name",
              labels={
                  "datetime" : "Date et heure", "production_mw" : "Production (MW)", "production_type": "Source","country_name": "Pays"
              })
st.plotly_chart(fig, width="stretch")

st.dataframe(df, width="stretch")
