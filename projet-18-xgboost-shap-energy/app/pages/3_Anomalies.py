import sys 
from pathlib import Path
import pandas as pd 
import plotly.express as px 
import streamlit as st 

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data"))
from train import train_models
from diagnose import diagnose

st.set_page_config(page_title="Diagnostic",page_icon="🔎",layout="wide")
st.title("🔎 Diagnostic énergétique")
st.caption("Identification des écarts de prévision et interprétation du modèle")

if st.button("Analyser les anomalies"):
    with st.spinner("Analyse en cours"):
        try:
            results = train_models()
            available_models = list(results.keys())
            preferred_models = "xgboost" if "xgboost" in available_models else available_models[0]
            diagnostics = diagnose(results,model_name=preferred_models)
            st.session_state["diagnostics"] = diagnostics
            st.session_state["diagnostic_model"] = preferred_models
            st.success(f"Diagnostic terminé avec le modèle : {preferred_models}")
        except Exception as e:
            st.error(f"Erreur pendant le diagnostic : {e}")

diagnostics = st.session_state.get("diagnostics")

if diagnostics is not None:
    if diagnostics.empty:
        st.warning("Aucun résultat à afficher")
        st.stop()

    c1,c2,c3 = st.columns(3)
    c1.metric("Nombre d'observations analysées",f"{len(diagnostics):,}")
    c2.metric("Ecart absolu moyen en MW",f"{diagnostics['erreur_absolue_mw'].mean():,.2f} MW")
    if "anomalie" in diagnostics.columns:
        c3.metric("Le nombre d'anomalies détectées",f"{int(diagnostics["anomalie"].sum())}")

    st.subheader("Résultats détaillés")
    st.dataframe(diagnostics,width="stretch")
    shap_path = ROOT / "outputs" / "shap_importance.png"

    st.subheader("Interprétabilité avec SHAP")

    if shap_path.exists():
        st.image(
            str(shap_path),
            caption="Importance globale des variables selon SHAP",
            width="stretch"
        )
    else:
        st.info(
            "Le graphique SHAP n'existe pas encore. "
            "Lance `python data/shape_analysis.py` depuis la racine du projet."
        )
else:
    st.info("Clique sur « Analyser les anomalies » pour commencer.")

