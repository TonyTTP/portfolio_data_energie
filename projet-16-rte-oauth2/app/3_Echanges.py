
import sqlite3
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st


st.title("Échanges transfrontaliers")
st.caption("Analyse des flux électriques impliquant la France")

# le fichier est dans app/, la base est dans projet-16-rte-oauth2/database/ donc on remonte de 2 crans
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "energy_oauth.db"
# 1. Chargement des données
# Importer les bibliothèques nécessaires.
# Se connecter à la base de données energy_oauth.db.
# Charger la table echanges dans un DataFrame Pandas.


@st.cache_data(ttl=300)
def load_echanges():
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query("SELECT * from echanges",conn)

df = load_echanges()
df["datetime"] = pd.to_datetime(df["datetime"]) # SQLite stocke les dates en texte
required = {"datetime","flow_mw","sender", "receiver"}

df = df[(df["sender"] == "FRANCE") | (df["receiver"] == "FRANCE")].copy()

df["direction"] = df.apply(lambda row: ("Import" if row["receiver"] == "FRANCE" else "Export"),axis=1,)

df["pays_partenaire"] = df.apply(lambda row: (row["sender"] if row["receiver"] == "FRANCE" else row["receiver"]),axis=1,)

# 3. Création des filtres
# Ajouter un filtre pour sélectionner le sens des échanges.
# Ajouter un filtre pour sélectionner les pays partenaires.
# Ajouter un filtre pour choisir une période.
# Afficher un avertissement si aucune donnée ne correspond
# aux filtres sélectionnés.

st.sidebar.title("Filtres")
directions = st.sidebar.multiselect("Sens du flux", options=["Import", "Export"], default=["Import","Export"])

pays = sorted(df["pays_partenaire"].unique())

pays_s =st.sidebar.multiselect("Pays partenaire", options=pays,default=pays)

date_min= df["datetime"].min().date()
date_max= df["datetime"].max().date()

periode = st.sidebar.date_input("Période", value=(date_min,date_max), min_value=date_min,max_value=date_max)

if isinstance(periode, (tuple, list)) and len(periode) == 2:
    debut, fin = periode
else:
    debut, fin = date_min, date_max

df = df[df["direction"].isin(directions) & df["pays_partenaire"].isin(pays_s)
    & (df["datetime"].dt.date >= debut) & (df["datetime"].dt.date <= fin)].copy()

if df.empty:
    st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
    st.stop()

# 4. Affichage des indicateurs
# Afficher le nombre de mesures disponibles.
# Afficher le nombre de pays partenaires.
# Calculer et afficher la puissance moyenne absolue des échanges
# en MW.

c1, c2, c3 = st.columns(3)
c1.metric("Nombre de mesures disponibles", f"{len(df):,}")
c2.metric("Nombre de pays partenaires", df["pays_partenaire"].nunique())
c3.metric("Puissance moyenne absolue", f"{df['flow_mw'].abs().mean():,.0f} MW")

st.divider()

st.subheader("Évolution des flux")

fig = px.line(df.sort_values("datetime"), x="datetime", y="flow_mw", color="pays_partenaire", line_dash="direction",
              title="Puissance des échanges par partenaire",
              labels={
                  "datetime" : "Date",
                  "flow_mw" : "Flux (MW)",
                  "pays_partenaire" : "Pays partenaire",
                  "direction" : "Sens",
              })
st.plotly_chart(fig, width="stretch")
st.subheader("Comparaison des partenaires")

resume = (
    df.assign(flux_absolu=df["flow_mw"].abs())
    .groupby(["pays_partenaire", "direction"], as_index=False)
    .agg(
        puissance_absolue_moyenne_mw=("flux_absolu", "mean"),
        puissance_maximale_absolue_mw=("flux_absolu", "max"),
        nombre_mesures=("flow_mw", "count"),
    )
)

fig = px.bar(
    resume,
    x="pays_partenaire",
    y="puissance_absolue_moyenne_mw",
    color="direction",
    barmode="group",
    title="Puissance absolue moyenne par partenaire",
    labels={
        "pays_partenaire": "Pays",
        "puissance_absolue_moyenne_mw": "Puissance moyenne absolue (MW)",
        "direction": "Sens",
    },
)
st.plotly_chart(fig, width="stretch")

st.dataframe(resume,width="stretch", hide_index=True)

st.download_button("Exporter les échanges filtrés",data=df.to_csv(index=False).encode("utf-8"),file_name="echanges_filtres.csv",
    mime="text/csv",)
