import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet

#je vais réaliser ma 1ère application via Streamlit
#Sujet : Analyse et prévision de la consommation et production au sein du territoire francais


# CONFIGURATION DE LA PAGE

st.set_page_config(
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

st.sidebar.title("Paramètres")

page = st.sidebar.radio("Navigation", ["Tableau de bord", "Prévisions", "Analyse"])

region = st.sidebar.selectbox("Région", ["Paris", "Lyon", "Marseille"])

periode = st.sidebar.slider("Periode (jours)", min_value=7, max_value=365, value=90)

type_graphique = st.sidebar.radio("Type de graphique", ["Ligne", "Barre", "Diffusion"])

#on va mettre en place un dataframe filtré poir filtré la region et la temporalité

df_filtre = df[df["region"] == region].tail(periode)


if page == "Tableau de bord" : 
    st.title("Tableau de Bord Energie France")
    col1, col2,col3,col4 = st.columns(4)
    col1.metric("Conso moyenne", f"{df_filtre["conso_mw"].mean():.0f} MW")
    col2.metric("Maximum", f"{df_filtre["conso_mw"].max():.0f} MW")
    col3.metric("Minimum", f"{df_filtre["conso_mw"].min():.0f} MW")
    variation = df_filtre["conso_mw"].iloc[-1] - df_filtre["conso_mw"].iloc[0]
    col4.metric("Variation ", f"{variation:+.0f} MW")

    st.subheader("Table brute")
    st.dataframe(df_filtre)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Consommation")
        if type_graphique == "Ligne":
            st.line_chart(df_filtre.set_index("date")["conso_mw"])
        elif type_graphique == "Barre" : 
            st.bar_chart(df_filtre.set_index("date")["conso_mw"])
        else:
            fig = px.scatter(df_filtre, x="date", y="conso_mw")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Mix Energétique")
        if type_graphique == "Ligne": 
            st.line_chart(df_filtre.set_index("date")[["prod_eolien","prod_nucleaire"]])
        elif type_graphique == "Barre":
            st.bar_chart(df_filtre.set_index("date")[["prod_eolien","prod_nucleaire"]])
        else: 
            fig = px.scatter(df_filtre, x="date", y=["prod_nucleaire","prod_eolien"])
            st.plotly_chart(fig, use_container_width=True)

    st.subheader("Répartition de l'énergie (camenbert)")
    fig_pie = px.pie(names=["Prod Eolien", "Prod Nucleaire"], values=[df_filtre["prod_eolien"].sum(),df_filtre["prod_nucleaire"].sum()])
    st.plotly_chart(fig_pie, use_container_width=True)

if page == "Prévisions": 
    st.title("Prévision Consommation")

    df_p = df[["date", "conso_mw"]].rename(columns={"date" : "ds", "conso_mw" : "y"})

    def train_model(data):
        modele = Prophet(yearly_seasonality=True)
        modele.fit(data)
        return modele

    nb_jours = st.number_input("Nombre de jours à prévoir", min_value=30,max_value=365,value=90)
    if st.button("Lancer la prévision"):
        with st.spinner("Prediction en cours"):
            modele = train_model(df_p)
            future = modele.make_future_dataframe(periods=nb_jours)
            prediction = modele.predict(future)

        st.success("Prediction terminée")
        st.line_chart(prediction.set_index("ds")[["yhat", "yhat_lower","yhat_upper"]])
        col1, col2, col3, col4 = st.columns(4)
        merged = df_p.merge(prediction[["ds","yhat"]], on="ds",how="inner")
        rmse = np.sqrt(np.mean((merged["y"] - merged["yhat"])**2))
        mape = np.mean(np.abs((merged["y"] - merged["yhat"]) / merged["y"])) * 100

        col1.metric("Prevision j+1",f"{prediction["yhat"].iloc[-1]:.0f} MW")
        col2.metric("Intervalle confiance", f"±{(prediction['yhat_upper'].iloc[-1] - prediction['yhat_lower'].iloc[-1])/2:.0f} MW")
        col3.metric("RMSE",f"{rmse:.0f} MW")
        col4.metric("MAPE",f"{mape:.0f} %")

if page == "Analyse":
    st.title("Analyse approfondie")   
    st.subheader("Correlation entre consommation et température")
    corr = px.scatter(df_filtre, x="temperature", y="conso_mw", trendline="ols")
    st.plotly_chart(corr,use_container_width=True)
    
    st.subheader("Anomalie de detection (>2*écartype)")
    moyenne = df_filtre["conso_mw"].mean()
    ecartype = df_filtre["conso_mw"].std()
    anomalie = df_filtre[np.abs(df_filtre["conso_mw"] - moyenne) > 2 * ecartype]
    fig_anom = go.Figure()
    fig_anom.add_trace(go.Scatter(x=df_filtre["date"],y=df_filtre["conso_mw"], mode="lines",name="Consommation"))
    fig_anom.add_trace(go.Scatter(x=anomalie["date"],y=anomalie["conso_mw"],mode="markers", name="Anomalie",marker=dict(color="red", size=10)))
    st.plotly_chart(fig_anom,use_container_width=True)

    st.subheader("Contribution de chaque ville")
    fig_region = px.box(df, x="region", y="conso_mw",color="region")
    st.plotly_chart(fig_region,use_container_width=True)
