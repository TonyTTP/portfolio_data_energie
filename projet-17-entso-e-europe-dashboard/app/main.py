
# app/main.py

from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


# Configuration de la page
st.set_page_config(
    page_title="ENTSO-E | Énergie européenne",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Énergie européenne")
st.caption(
    "Analyse de la consommation, de la production "
    "et des prix de l'électricité"
)


# Chemin vers la base SQLite
ROOT_DIR = Path(__file__).resolve().parents[1]
DB_PATH = ROOT_DIR / "database" / "energy_oauth.db"


# Fonction de chargement des données
@st.cache_data(ttl=300)
def load_data(table):
    # Autorise uniquement les trois tables prévues
    allowed_tables = {
        "entsoe_load",
        "entsoe_generation",
        "entsoe_prices"
    }

    if table not in allowed_tables:
        raise ValueError("Table non autorisée")

    if not DB_PATH.exists():
        return pd.DataFrame()

    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(
            f"SELECT * FROM {table}",
            conn
        )


# Chargement des trois tables
df_load = load_data("entsoe_load")
df_generation = load_data("entsoe_generation")
df_prices = load_data("entsoe_prices")


# Message si les données ne sont pas disponibles
if (
    df_load.empty
    and df_generation.empty
    and df_prices.empty
):
    st.info(
        "La base est vide. Lance la collecte ENTSO-E "
        "pour afficher les indicateurs."
    )
    st.stop()


# Filtres communs
countries = sorted(set(
    df_load.get("country_name", pd.Series(dtype=str))
    .dropna()
    .tolist()
    + df_generation.get(
        "country_name", pd.Series(dtype=str)
    ).dropna().tolist()
    + df_prices.get(
        "country_name", pd.Series(dtype=str)
    ).dropna().tolist()
))

selected_countries = st.multiselect(
    "Pays à analyser",
    options=countries,
    default=countries[:4]
)


# Filtrage des DataFrames
if not df_load.empty:
    df_load = df_load[
        df_load["country_name"].isin(selected_countries)
    ]

if not df_generation.empty:
    df_generation = df_generation[
        df_generation["country_name"].isin(
            selected_countries
        )
    ]

if not df_prices.empty:
    df_prices = df_prices[
        df_prices["country_name"].isin(
            selected_countries
        )
    ]


# Indicateurs principaux
col1, col2, col3 = st.columns(3)

with col1:
    # Moyenne des observations de consommation
    moyenne = (
        df_load["conso_mw"].mean()
        if not df_load.empty else None
    )
    st.metric(
        "Consommation moyenne",
        f"{moyenne:,.0f} MW" if pd.notna(moyenne)
        else "N/D"
    )

with col2:
    # Somme des observations de production
    production = (
        df_generation["production_mw"].sum()
        if not df_generation.empty else None
    )
    st.metric(
        "Production cumulée",
        f"{production:,.0f} MW" if pd.notna(production)
        else "N/D"
    )

with col3:
    # Moyenne des prix observés
    prix = (
        df_prices["price_eur_mwh"].mean()
        if not df_prices.empty else None
    )
    st.metric(
        "Prix spot moyen",
        f"{prix:,.2f} €/MWh" if pd.notna(prix)
        else "N/D"
    )


# Graphiques principaux
left, right = st.columns(2)

with left:
    st.subheader("📈 Évolution de la consommation")

    if not df_load.empty:
        fig = px.line(
            df_load,
            x="datetime",
            y="conso_mw",
            color="country_name",
            labels={
                "datetime": "Date",
                "conso_mw": "Consommation (MW)",
                "country_name": "Pays"
            },
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de consommation.")

with right:
    st.subheader("🌱 Production par filière")

    if not df_generation.empty:
        mix = (
            df_generation.groupby("production_type")
            ["production_mw"]
            .sum()
            .reset_index()
        )

        fig = px.pie(
            mix,
            names="production_type",
            values="production_mw",
            hole=0.45,
            labels={
                "production_type": "Filière",
                "production_mw": "Production cumulée (MW)"
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de production.")


# Tableau récapitulatif
st.subheader("📋 Aperçu des consommations")

if not df_load.empty:
    st.dataframe(
        df_load.sort_values("datetime", ascending=False),
        use_container_width=True,
        hide_index=True
    )
