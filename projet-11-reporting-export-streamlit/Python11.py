
#  Dashboard Énergie France — App Streamlit 3 "pages"

import streamlit as st
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from fpdf import FPDF

# Configuration de la page 


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
    df_export = df[["date","region","conso_mw","temperature"]]
    return df_export.to_csv(index=False, sep=";", encoding="utf-8-sig").encode("utf-8-sig")

#generer un pdf

def generate_pdf(df,region,moy,pic):
    pdf = FPDF()
    pdf.add_page()
    #en tete
    pdf.set_font("Arial","B",18)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,12,"Rapport Energie",ln=True,align="C")
    ln(4)

    pdf.set_font("Arial","",13)
    pdf.set_text_color(100,100,100)
    pdf.cell(0,12, f"Region : {region}", ln=True,align="C")
    pdf.cell(0,12, f"Génère le {pd.Timestemp.now().strftime('%d-%m-%Y) à %H-%M')}", ln=True,align="C")
    ln(8)

    pdf.set_draw_color(0,0,0)
    pdf.line(10, pdf.get_y(),200,pdf.get_y())
    ln(8)

    pdf.set_font("Arial","B",13)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,12, f"Indicateurs clés", ln=True)
    ln(2)

    pdf.set_font("Arial","",11)
    pdf.set_text_color(240,240,240)
    pdf.cell(95,10, "Consommation moyenne",border=1,fill=True)
    pdf.cell(95,10,f"{moy:.0f}", ln=True, fill=False)
    pdf.cell(95,10,"Pic maximum", border=1, fill=True)
    pdf.cell(95,10,f"{pic:.0f}", ln=True, fill=False)
    ln(10)

    pdf.set_font("Arial","B",14)
    pdf.set_text_color(0,0,0)
    pdf.cell(0,12,"Extrait des donnees (10 premieres lignes)", ln=True)

    headers = ["Date","Région","Conso (MW)", "Temp (°C)"]
    widths = [50,50,50,50]

    pdf.set_font("Arial","",12)
    pdf.set.set_text_color(255,255,255)
    pdf.set_fill_color(50,90,150)

    for header, width in zip(headers,widths):
        pdf.cell(width,8,header,border=1,fill=True, align="C")
    pdf.ln()

        # Lignes du tableau
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 0)

    for i, (_, row) in enumerate(df.head(10).iterrows()):
        fill = (i % 2 == 0)
        if fill:
            pdf.set_fill_color(245, 245, 245)

        pdf.cell(width[0],8,row["date"].strftime("%d/%m/%Y"), border=1,fill=fill)
        pdf.cell(width[1],8,row["region"], border=1, fill=fill)
        pdf.cell(width[2],8,f"{row["conso_mw"]:.0f}", border=1, fill=fill)
        pdf.cell(width[3],8,f"{row["temperature"]:.0f}", border=1, fill=fill)
        pdf.ln()

    return bytes(pdf.output(dest="S"))


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


df = charge_donnee()

st.title("Dashboard Energie France")

st.markdown("""Bienvenue sur le tableeau de bord de consommation électrique francaise
**Navigation** : utiliser le menu à gauche""")

page = st.sidebar.radio("Page", ["Dashboard","Prévisions","Analyse"])

st.sidebar.markdown("---")

region_filtree = st.sidebar.multiselect("Filtrer par region", options=df["region"].unique(), default=list(df["region"].unique()))
date_filtree = st.sidebar.date_input("Filtre par région", value=(df["date"].min(), df["date"].max()), min_value=df["date"].min(),max_value=df["date"].max())

# j'application des filtres 
df_filtre = df[df["region"].isin(region_filtre)]
if isinstance(periode, tuple) and len(periode) == 2:
    debut, fin = pd.to_datetime(periode[0]), pd.to_datetime(periode[1])
    df_filtre = df_filtre[(df_filtre["date"] >= debut) & (df_filtre["date"] <= fin)]

if model not in st.session_state:
    st.session_state.model = None
if forecast not in st.session_state:
    st.session_state.forecast = None
if rmse not in st.session_state:
    st.session_state.rmse = None
if mape not in st.session_state: 
    st.session_state.mape = None


if page == "Dashboard": 
    st.header("Analyse")
    df_sorted = df.sort_values("date")
    if len(df_sorted) >= 14 : 
        semaine_actuelle = df_sorted.tail(7).mean()
        semaine_precedente = df_sorted.tail(14).head(7).mean()
        delta = semaine_actuelle - semaine_precedente
    else: 
        semaine_actuelle = df_sorted["conso_mw"].mean() if len(df_sorted) else 0
        delta = 0
    col1,col2,col3 = st.columns(3)
    col.metric("Conso moyenne (7 derniers jours)",f"{df_filtre["conso_mw"].mean()}MW")
    col2.metric("Pic maximum",f"{df_filtre["conso_mw"].max()} MW")
    col3.metric("Nombre de jours affichés",f"{len(df_filtre)}")

    st.plotly_chart(graph_ligne_conso(df_filtre), use_container_width=True)
    st.plotly_chart(graph_barres_empilees(df_filtre), use_container_width=True)

    st.subheader("Tableau comparatif régions")
    tableau_regions = (
    df_filtre.groupby("region")["conso_mw"].agg(["mean", "max", "min", "std"])
        .rename(columns={"mean": "Moyenne", "max": "Max", "min": "Min", "std": "Écart-type"})
        .round(0)
    )
    st.dataframe(tableau_regions, use_container_width=True)







