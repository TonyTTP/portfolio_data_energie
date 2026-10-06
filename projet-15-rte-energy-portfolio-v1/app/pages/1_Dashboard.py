import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

DATABASE = "database.db"

st.title("Dashboard Energie France")

@st.cache_data(ttl=1800)
def load_dashboard_data():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql(
        """
    SELECT * FROM v_dashboard
    ORDER BY date_heure
""", conn)
    conn.close()
    return df

df = load_dashboard_data()

@st.cache_data(ttl=1800)
def load_dashboard_kpi():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql(
        """
    SELECT * FROM v_kpi
""", conn)
    conn.close()
    return df

kpi = load_dashboard_kpi()

c1,c2,c3,c4 = st.columns(4)

c1.metric("Moyenne de la consommation", f"{kpi['moy_conso'].iloc[0]:.2f} MW")

c2.metric("Pic de consommation", f"{kpi['max_conso'].iloc[0]:.2f} MW")

c3.metric("Part énergie renouvelable",f"{kpi['part_moy_renouv_pct'].iloc[0]:.2f} %")

c4.metric("CO2 moyen",f"{kpi['moy_co2'].iloc[0]:.2f} gCO₂/kWh")

st.divider()

st.subheader("Evolution de la consommation dans le temps")

fig = px.line(df.tail(200),x="date_heure",y="consommation",title="Graphique de la consommation en fonction du temps",
              labels={"date_heure" : "Date", "consommation" : "MW"})

st.plotly_chart(fig, width="stretch")

st.divider()

st.subheader("Répartition des énergies")

mix = {
        "Solaire" : df["solaire"].mean(),
        "Nucléaire" : df["nucleaire"].mean(),
        "Eolien" : df["eolien"].mean(),
        "Hydraulique" : df["hydraulique"].mean()
}

fig_mix = px.pie(values=list(mix.values()),names=list(mix.keys()),
                 title="Production moyenne par source")

st.plotly_chart(fig_mix,width="stretch")

st.divider()

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Télécharger les données",
    csv,
    "energie_france.csv",
    "text/csv"
)
