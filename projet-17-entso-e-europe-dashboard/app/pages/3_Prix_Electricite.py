import pandas as pd
import sqlite3
import streamlit as st
from pathlib import Path
import plotly.express as px

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR / "database" / "energy_oauth.db"

st.set_page_config(
    page_icon="💶",
    page_title="Prix de l'électricité",
    layout="wide"
)

st.title("Prix de l'électricité en Europe")
st.caption("Analyse des prix de gros sur le marché journalier")

@st.cache_data(ttl=300)
def load_data():
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query("SELECT * FROM entsoe_prices", conn)

try:
    df = load_data()
except Exception as error:
    st.error(f"Erreur de chargement : {error}")
    st.stop()

df["datetime"] = pd.to_datetime(df["datetime"], utc=True, errors="coerce")

df["price_eur_mwh"] = pd.to_numeric(df["price_eur_mwh"], errors="coerce")

df = df.dropna(subset=["datetime", "price_eur_mwh"])

st.sidebar.header("Filtres")

countries  = sorted(df["country_name"].dropna().unique())
countries_selected = st.sidebar.multiselect("Pays",options=countries, default=countries[:3])

df = df[df["country_name"].isin(countries_selected)]

if df.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

col1, col2, col3 = st.columns(3)

col1.metric("Prix moyen", f"{df['price_eur_mwh'].mean():.2f} €/MWh")
col2.metric("Prix maximum", f"{df['price_eur_mwh'].max():.2f} €/MWh")
col3.metric("Prix minimum", f"{df['price_eur_mwh'].min():.2f} €/MWh")

st.subheader("Évolution du prix de l'électricité")

fig_line = px.line(
    df.sort_values("datetime"),
    x="datetime",
    y="price_eur_mwh",
    color="country_name",
    labels={
        "datetime": "Date et heure",
        "price_eur_mwh": "Prix (€/MWh)",
        "country_name": "Pays"})

st.plotly_chart(fig_line, width="stretch")

st.subheader("Comparaison des prix moyens par pays")

price_comparison = (df.groupby("country_name", as_index=False)["price_eur_mwh"]
    .mean()
    .sort_values("price_eur_mwh", ascending=True))

fig_bar = px.bar(
    price_comparison,
    x="country_name",
    y="price_eur_mwh",
    labels={
        "country_name": "Pays",
        "price_eur_mwh": "Prix moyen (€/MWh)"})

st.plotly_chart(fig_bar, width="stretch")
