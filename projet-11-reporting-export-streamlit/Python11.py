import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from prophet import Prophet
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error


st.set_page_config(page_icon="🌞",page_title="Dashbord France",layout="wide")

st.title("Tableau de bord énergétique de la France")
st.write("Navigation : utiliser le menu à gauche")


@st.cache_data
def charger_donnees():

    np.random.seed(42)

    dates = pd.date_range("2023-01-01", periods=365)

    df = pd.DataFrame({
        "date": dates,
        "conso_mw": (
            45000
            + 8000 * np.cos(np.linspace(0, 2 * np.pi, 365))
            + np.random.normal(0, 1000, 365)
        ),
        "region": np.tile(
            ["Paris", "Lyon", "Marseille"],
            122
        )[:365],
        "temperature": (
            10
            + 12 * np.cos(np.linspace(0, 2 * np.pi, 365))
        )
    })

    anomalies = np.random.choice(df.index, 8, replace=False)
    df.loc[anomalies, "conso_mw"] += np.random.choice(
        [-6000, 7000],8)
    


    return df

df = charger_donnees()


st.sidebar.header("Filtres")

page = st.sidebar.radio("Page", ["Dashboard","Prévisions","Analyse"])

regions = st.sidebar.multiselect("region", df["region"].unique(), default=list(df["region"].unique()))


periodes = st.sidebar.date_input("Période",value=(df["date"].min(),df["date"].max()),min_value=df["date"].min(),max_value=df["date"].max())

df_filtre = df[df["region"].isin(regions)]

if len(periodes) == 2 : 
    debut = pd.to_datetime(periodes[0])
    fin = pd.to_datetime(periodes[1])

    df_filtre = df_filtre[(
        df_filtre["date"] >= debut) & (df_filtre["date"] <= fin )]

if page == "Dashboard": 
    st.subheader("Dashboard")

    df_filtre = df_filtre.sort_values("date")

    col1,col2,col3 = st.columns(3)

    if len(df_filtre) >= 14:
        moyenne_actuelle = df_filtre.tail(7)["conso_mw"].mean()
        moyenne_precedente = df_filtre.tail(14).head(7)["conso_mw"].mean()
        delta = moyenne_actuelle - moyenne_precedente
    else: 
        moyenne_actuelle = df["conso_mw"].mean()
        delta=0

    col1.metric("Conso moyenne (7 derniers jours)", f"{moyenne_actuelle:.0f} MW", f"{delta:.0f} MW")
    col2.metric("Pic maximal",f"{df_filtre['conso_mw'].max():.0f} MW")
    col3.metric("Nombre de jours",len(df_filtre))

    fig = px.line(df_filtre, x="date", y="conso_mw", color="region",title="Consommation électrique par région")
    st.plotly_chart(fig,use_container_width=True)

    df_mois = df_filtre.copy()

    df_mois["mois"] = df_mois["date"].dt.to_period("M").astype(str)

    df_mois = df_mois.groupby(["region","mois"], as_index=False)["conso_mw"].mean()

    fig = px.bar(df_mois,x="mois",y="conso_mw", color="region",title="Mix énergétique mensuel par région")

    st.plotly_chart(fig, use_container_width=True)

    tableau = (df_filtre.groupby("region")["conso_mw"].agg(["mean","max","min","std"]).rename(columns={"mean" : "moyenne", "max" : "Maximum","min" : "Minimum", "std" : "écart-type"}).round(0))

    st.dataframe(tableau,use_container_width=True)

elif page == "Prévisions":

    st.header("Prévisons")
    jour = st.slider("Nombre de jour à prévoir", 7, 90,30)

    data_prophet = df_filtre.groupby("date",as_index=False)["conso_mw"].mean().rename(columns={"date" : "ds", "conso_mw" : "y"})

    if st.button("Lancer la prévision"):

        with st.spinner("En cours d'éxecution.."): 
            model = Prophet()
            model.fit(data_prophet)

            future = model.make_future_dataframe(periods=jour)

            prevision = model.predict(future)

            comparaison = prevision[["ds","yhat"]].merge(data_prophet,on="ds")

            rmse = np.sqrt(mean_squared_error(comparaison["y"], comparaison["yhat"]))

            mape = mean_absolute_percentage_error(comparaison["y"],comparaison["yhat"])

        col1,col2 = st.columns(2)

        col1.metric("RMSE", f"{rmse:.0f} MW")
        col2.metric("MAPE", f"{mape * 100:.0f} %")

        st.subheader(f"Prévision sur {jour} jours")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=prevision["ds"],
            y=prevision["yhat_lower"],
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=prevision["ds"],
            y=prevision["yhat_upper"],
            fill="tonexty",
            name= "Intervalle de confiance"
        ))

        fig.add_trace(go.Scatter(
            x= prevision["ds"],
            y= prevision["yhat"],
            name="Prévision"
        ))

        st.plotly_chart(fig, use_container_width=True)
    


elif page == "Analyse" : 
    st.header("Analyse")

    fig = px.scatter(
        df_filtre,
        x="temperature",
        y="conso_mw",
        title="Consommation vs Température",
        color="region"
    )

    st.plotly_chart(fig, use_container_width=True)

    repartition = df_filtre.groupby("region", as_index=False)["conso_mw"].sum()

    fig = px.pie(
        repartition, 
        names="region",
        values="conso_mw",
        title="Répartion de la consommation par région"
    )
    st.plotly_chart(fig, use_container_width=True)
    

    correlation = df_filtre[["conso_mw","temperature"]].corr()

    fig = px.imshow(
        correlation,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title = "Corrélation de la consommation/température"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Top 10 anomalies")

    anomalies = df_filtre.sort_values("date").copy()

    anomalies["moyenne_mobile"] = anomalies["conso_mw"].rolling(7,min_periods=1).mean()
    anomalies["ecart"] = (anomalies["moyenne_mobile"] - anomalies["conso_mw"]).abs()
    top10 = anomalies.sort_values("ecart",ascending=False).head(10)

    st.dataframe(top10[["date","region","conso_mw","moyenne_mobile","ecart"]].round(0),use_container_width=True)

    st.subheader("export")

    csv = df_filtre[["date", "conso_mw", "temperature"]].to_csv(index=False, sep=";", encoding="utf-8-sig")

    st.download_button("Télécharger les données en csv", csv, "conso_energie.csv")