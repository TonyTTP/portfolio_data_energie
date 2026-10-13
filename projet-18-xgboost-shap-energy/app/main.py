
import streamlit as st

st.set_page_config(
    page_title="Energy Diagnostic",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Energy Diagnostic")
st.subheader("Prévision et diagnostic de la consommation électrique")

st.markdown("""
Bienvenue sur **Energy Diagnostic**, un outil d'analyse de la consommation électrique
basé sur les données historiques et météorologiques.

### Les fonctionnalités

- **Dashboard** : suivre la consommation électrique et les données météo.
- **Prévisions** : entraîner des modèles Machine Learning et comparer leurs performances.
- **Anomalies** : repérer les erreurs de prévision et comprendre les facteurs explicatifs avec SHAP.
""")

st.info(
    "Commence par le Dashboard pour explorer les données, "
    "puis passe aux Prévisions et au Diagnostic."
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Technologie", "Python + SQL")

with col2:
    st.metric("Machine Learning", "Random Forest / XGBoost")

with col3:
    st.metric("Interprétabilité", "SHAP")
