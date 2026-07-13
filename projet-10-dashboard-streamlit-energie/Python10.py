import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet

#je vais réaliser ma 1ère application via Streamlit
#Sujet : Analyse et prévision de la consommation et production au sein du territoire francais


# CONFIGURATION DE LA PAGE

st.page_config(
    page_title="Dashboard RTE (simulation)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

#Données simulées RTE en france

np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=365)
df = pd.DataFrame({
    "date"           : dates,
    "conso_mw"       : 45000 + 8000*np.cos(np.linspace(0, 2*np.pi, 365)) + np.random.normal(0, 1000, 365),
    "prod_nucleaire"  : 35000 + np.random.normal(0, 1500, 365),
    "prod_eolien"    : 5000  + np.random.normal(0, 800,  365),
    "temperature"    : 10 + 12*np.cos(np.linspace(0, 2*np.pi, 365)),
    "region"         : np.tile(["Paris","Lyon","Marseille"], 122)[:365]
})

st.sidebar_title("Paramètre")

page = st.sidebar.radio("Navigation", [["Tableau de bord","Prévisions","Analyse"]])

region = st.sidebar.selectbox("Region", [["Paris","Lyon","Marseille"]])

periode = st.sidebar.slider("Periode (jours)", min_value=7, max_value=365, value=90)

type_graphique = st.sidebar.radio("Type de graphique", [["Ligne","Barre","Diffusion"]])

#on va mettre en place un dataframe filtré poir filtré la region et la temporalité

df_filtre = df[df["region"] == region].tail(periode)