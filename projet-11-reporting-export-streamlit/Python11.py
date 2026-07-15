
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
    return df.to_csv(index=False).encoding("utf-8")

#generer un pdf

def convert_to_csv(df, region,moy,pic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16)
    pdf.cell(200,10, f"Rapport énergie - {region}",ln=True,align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200,10, f"Moyenne : {moy:.0f} MW",ln=True)
    pdf.cell(200,10, f"Pic : {pic:.0f} MW",ln=True)
    pdf.output(dest="S").encode("latin-1")


