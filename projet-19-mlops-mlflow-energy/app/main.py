
import streamlit as st

st.set_page_config(
    page_title="TD19 - MLOps Energy",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Energy Forecasting & MLOps")
st.markdown(
    """
    ### Bienvenue sur le tableau de bord énergétique

    Cette application permet de :
    - Visualiser les données de consommation électrique RTE.
    - Consulter les prévisions du modèle XGBoost.
    - Comparer les expériences MLflow et leurs performances.

    Utilise le menu latéral pour naviguer entre les pages.
    """
)

st.info(
    "Sélectionne une page dans le menu à gauche pour commencer."
)
