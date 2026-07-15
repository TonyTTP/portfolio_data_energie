
#  Dashboard Énergie France — App Streamlit 3 "pages"

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from fpdf import FPDF

# Configuration de la page 

st.set_page_config(
    page_icon="⚡",
    page_title="Dashboard RTE",
    layout="wide"
)

@st.cache_data
def charger_donnees():
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=365)

    df = pd.DataFrame({
        "date": dates,
        "conso_mw": 45000 + 8000 * np.cos(
                        np.linspace(0, 2 * np.pi, 365))
                    + np.random.normal(0, 1000, 365),
        "region": np.tile(["Paris", "Lyon", "Marseille"], 122)[:365],
        "temperature": 10 + 12 * np.cos(
                        np.linspace(0, 2 * np.pi, 365))
    })

    # petites anomalies 
    idx_anomalies = np.random.choice(df.index, size=8, replace=False)
    df.loc[idx_anomalies, "conso_mw"] += np.random.choice([-6000, 7000], size=8)

    return df

#fonction convertir en csv

def convert_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")

#generer un pdf

def generate_pdf(df,region,moy,pic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial",size=16)
    pdf.cell(200,10,f"Rapport Energie - {region}", ln=True,align="C")
    pdf.set_font("Arial",size=12)
    pdf.cell(200,10,f"Moyenne : {moy}", ln=True)
    pdf.cell(200,10,f"Pic : {pic} MW", ln=True)
    pdf.output(dest="S").encode("latin-1")

def graph_ligne_conso(df):
    fig = px.line(
        x="date",
        y="conso_mw",
        labels={"date" : "Date", "conso_mw" : "Conso en MW"},
        color="region",
        title="Conso électrique par region"
    )
    return fig

def correlation(df):
    fig = pix.scatter(
    x = "temperature",
    y = "conso_mw",
    trendline = "ols",
    labels={"temperature" : "Temperature en °C", "conso_mw" : "Conso en MW"},
    color="region",
    title="Courbe de correlation entre Consommation et température"
    )
    return fig

def barre_empilee(df):
    df_mensuel = (df.assign(mois=df["date"].dt.to_period("M").astype(str)).groupby(["region","mois"])["conso_mw"].mean())
    fig = pix.bar(
        df_mensuel,
        x = "mois",
        y="conso_mw",
        barmode="stack",
        color="region",
        title="Graphe de la moyenne conso par region"
    )
    return fig

def camembert(df):
    df_mix = df.groupby("region")["conso_mw"].mean()
    fig = px.pie(
        df_mix,
        names="region",
        values="conso_mw",
        title="Répartition du mix énergétique"
    )
    return df

def heat_map(df): 
    corr = [["conso_mw","temperature"]].corr()
    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Heatmap des corrélations"
    )
    return df






