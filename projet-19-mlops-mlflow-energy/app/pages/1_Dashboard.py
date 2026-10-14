import sqlite3
from pathlib import Path 
import pandas as pd 
import plotly.express as px 
import streamlit as st 

ROOT_DIR = Path(__file__).resolve().parents[2]
DB_PATH = ROOT_DIR/"database"/"energy.db"

st.title("⚡ Dashboard énergétique")
st.caption("Source : données Eco2Mix de RTE")

if not DB_PATH.exists():
    st.error("Base de données introuvable, il faut lancer store.py")
    st.stop()

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("""SELECT date_heure,consommation,nucleaire,eolien,
                       solaire,hydraulique,taux_co2
                       FROM eco2mix
                       ORDER BY date_heure""",conn)

if df.empty:
    st.warning("Aucune donnée disponible")
    st.stop()

df["date_heure"] = pd.to_datetime(df["date_heure"])

c1,c2,c3 = st.columns(3)

c1.metric("Consommation moyenne en MW", f"{df["consommation"].mean():.0f} MW")
c2.metric("Consommation maximale en MW", f"{df["consommation"].max():.0f} MW")
c3.metric("Taux de CO2 moyen", f"{df["taux_co2"].mean():.1f} g CO₂/kWh" 
          if df["taux_co2"].notna().any() else "N/A")

st.subheader("Evolution de la consommation")

fig = px.line(df, x="date_heure", y="consommation", title="Consommation électrique dans le temps",
              labels= {
                  "date_heure" : "Date",
                  "consommation" : "Consommation (MW)"
              })
st.plotly_chart(fig, width="stretch")

st.subheader("Mix énergétique")

mix_cols = [c for c in ["nucleaire","eolien","solaire","hydraulique"] if c in df.columns and df[c].notna().any()]

if mix_cols:
    mix = df[mix_cols].mean().rename_axis("Filière").reset_index(
        name="Production moyenne (MW)")

    fig_mix = px.bar(
        mix,
        x="Filière",
        y="Production moyenne (MW)",
        title="Production moyenne par filière",
    )

    st.plotly_chart(fig_mix, width="stretch")

st.dataframe(df.tail(20), width="stretch")
