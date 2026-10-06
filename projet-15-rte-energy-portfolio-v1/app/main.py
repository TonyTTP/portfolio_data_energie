import streamlit as st 

st.set_page_config(
    page_icon="⚡",
    page_title="Energie France",
    layout="wide"
)

st.title("Dashboard Energie France")

st.divider()

st.markdown(
        """
    ## Bienvenue sur le projet RTE Energy 

    Cette application permet d'analyser :

    - la consommation électrique française ,
    - le mix énergétique ,
    - les prévisions de consommation ,
    - les anomalies détectées.

    Utilisez le menu à gauche pour naviguer
    entre les différentes sections.
    """
)



