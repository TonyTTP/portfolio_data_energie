# les import plein
#mettre un titre
#petit texte gris
#mettre le chemin
#créer le post it
#fonction charger les données de production
#écrire la dataframe pour récupérer la prod sans total
#créer le filtre de type de production des filières sans doublons et triée par ordre alphabétique.
# et temporalité

import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from pathlib import Path

st.title("Analyse de production")
st.caption("Comparaison des filières de production électrique")

# le fichier est dans app/, la base est dans projet-16-rte-oauth2/database/ donc on remonte de 2 crans
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "energy_oauth.db"

@st.cache_data(ttl=300)
def load_production():
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query("SELECT * FROM production", conn)

df = load_production()
df = df[df["production_type"] != "TOTAL"]
df["datetime"] = pd.to_datetime(df["datetime"]) # SQLite stocke les dates en texte

st.sidebar.header("Filtres")

filtres = sorted(df["production_type"].unique())

filieres_sel = st.sidebar.multiselect("Filières",options=filtres,default=filtres)

date_min = df["datetime"].min().date()
date_max = df["datetime"].max().date()

periode = st.sidebar.date_input("Période", value=(date_min,date_max),min_value=date_min, max_value=date_max)

if isinstance(periode, (tuple, list)) and len(periode) == 2:
    debut, fin = periode
else:
    debut, fin = date_min, date_max

df = df[df["production_type"].isin(filieres_sel) & (df["datetime"].dt.date >= debut)
        & (df["datetime"].dt.date <= fin)].copy()

if df.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

production_max = df["production_mw"].max()

production_moyenne = df.groupby("datetime")["production_mw"].sum().mean()

filiere_principale = df.groupby("production_type")["production_mw"].sum().idxmax()

#3 metric production horaire moyenne production max filere dominance barre horizontal sous titre

c1,c2,c3 = st.columns(3)

c1.metric("Production horaire moyenne", f"{production_moyenne:,.0f} MW")
c2.metric("Production maximale", f"{production_max:,.0f} MW")
c3.metric("Filière dominante", filiere_principale)

st.divider()

st.subheader("Évolution temporelle")

fig = px.line(df.sort_values("datetime"), x="datetime", y="production_mw",color="production_type", title="Production par filière",
              labels= {
                  "datetime" : "Date", "production_mw" : "Production en MW", "production_type" : "Filières"
              })

st.plotly_chart(fig, width="stretch")

st.subheader("Répartition de la puissance des différentes filières")

comparaison = (df.groupby("production_type", as_index=False).agg(
        moyenne_mw=("production_mw", "mean"),
        maximum_mw=("production_mw", "max"),
        nombre_mesures=("production_mw", "count"),).sort_values("moyenne_mw", ascending=False))

fig = px.bar(comparaison, x="production_type", y="moyenne_mw", title="Production moyenne par filière",
             labels= {"production_type" : "Filières","moyenne_mw" : "Production moyenne (MW)"})

st.plotly_chart(fig, width="stretch")

st.dataframe(comparaison,width="stretch",hide_index=True)

st.download_button(
    "Télécharger les données filtrées",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="production_filtrees.csv",
    mime="text/csv",
)
