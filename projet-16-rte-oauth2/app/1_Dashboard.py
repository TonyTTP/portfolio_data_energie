# les import plein
import pandas as pd
from pathlib import Path
import streamlit as st
import sqlite3
import plotly.express as px

st.title("Dashboard énergétique")

st.caption("Vue générale du système électrique français")

DB_PATH = Path(__file__).resolve().parent.parent / "database" / "energy_oauth.db"
#créer le post it
@st.cache_data(ttl=300)
def load_data(table):
    conn = sqlite3.connect(DB_PATH)
    return pd.read_sql_query(f"SELECT * FROM {table}", conn)

try:
    conso = load_data("consommation")
    prod = load_data("production")
    echanges = load_data("echanges")
except Exception as error:
    st.error(f"Erreur de chargement : {error}")
    st.stop()

if conso.empty and prod.empty and echanges.empty:
    st.warning("Aucune donnée disponible")
    st.stop()


for df in (conso, prod, echanges):
    df["datetime"] = pd.to_datetime(df["datetime"])

st.sidebar.header("Filtres")

date_min = min(df["datetime"].min() for df in (conso, prod, echanges) if not df.empty).date()
date_max = max(df["datetime"].max() for df in (conso, prod, echanges) if not df.empty).date()



periode = st.sidebar.date_input("Période", value=(date_min,date_max), min_value=date_min, max_value=date_max)

if isinstance(periode, (tuple, list)) and len(periode) == 2:
    debut, fin = periode
else:
    debut, fin = date_min, date_max

filieres = sorted(prod.loc[prod["production_type"] != "TOTAL", "production_type"].unique())
filieres_selectionnees = st.sidebar.multiselect("Filières", options=filieres, default=filieres)


conso = conso[conso["datetime"].dt.date.between(debut, fin)]
prod = prod[prod["datetime"].dt.date.between(debut, fin)]
echanges = echanges[echanges["datetime"].dt.date.between(debut, fin)]

prod = prod[prod["production_type"].isin(filieres_selectionnees)] 


c1,c2,c3,c4  = st.columns(4)


conso_reelle = conso[conso["type"] == "REALISED"] if "type" in conso.columns else conso

#si conso réelle est pas vide affichée la moyenne et le pic sinon NA
if not conso_reelle.empty:
    c1.metric("Consommation moyenne", f"{conso_reelle['conso_mw'].mean():,.0f} MW")
    c2.metric("Pic de consommation", f"{conso_reelle['conso_mw'].max():,.0f} MW")
else:
    c1.metric("Consommation moyenne", "N/A")
    c2.metric("Pic de consommation", "N/A")

if not prod.empty:
    prod_totale_par_heure = prod.groupby("datetime")["production_mw"].sum()
    prod_moyenne = prod_totale_par_heure.mean()
    c3.metric("Production totale moyenne",f"{prod_moyenne:,.0f} MW")
else:
    c3.metric("Production totale moyenne", "N/A")

if not echanges.empty:
    c4.metric("Lignes d'échanges", f"{len(echanges):,}")
else:
    c4.metric("Lignes d'échanges", "N/A")

st.divider()


st.subheader("Évolution de la consommation")


fig = px.line(conso_reelle.sort_values("datetime"),x="datetime", y="conso_mw",title="Consommation électrique",
              labels={
                  "datetime" : "Date",
                  "conso_mw" : "Consommation (MW)"})

st.plotly_chart(fig, width="stretch")


st.subheader("Production par filière")


production_filiere = prod.groupby("production_type", as_index=False)["production_mw"].sum()

fig = px.pie(production_filiere, names="production_type",values="production_mw",title="Répartition des valeurs de production", hole=0.4)

st.plotly_chart(fig, width="stretch")
