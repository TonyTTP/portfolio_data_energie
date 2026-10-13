import sys
from pathlib import Path
import pandas as pd 
import plotly.express as px
import streamlit as st 

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "data"))
from train import train_models


st.set_page_config(page_title="Prévisions",page_icon="🔮", layout="wide")
st.title("Prévisions de consommation")
st.caption("Entraînement et comparaison des modèles de Machine Learning")
st.markdown("Objectif : prévoir la consommation à partir de l'historique, de la météo et des variables temporelles.")

if st.button("🚀 Entraîner les modèles",type="primary"):
    with st.spinner("Chargement..."):
        try:
            results = train_models()
            st.session_state["model_results"] = results 
            st.success("Entrainement terminé")
        except Exception as e:
            st.error(f"Impossible d'entrainer le modele : {e}")

results = st.session_state.get("model_results")

if results:
    comparison = pd.DataFrame([{"modele": name,
                                "RMSE" : result["rmse"],
                                "R²" : result["r2"]}
                                for name, result in results.items()
                                ])

    st.subheader("Comparaison des performances")
    st.dataframe(
        comparison.style.format({"RMSE": "{:.2f}", "R²": "{:.3f}"}),
        width="stretch"
    )

    best_model = comparison.loc[comparison["RMSE"].idxmin()]

    c1, c2 = st.columns(2)
    c1.metric("Meilleur modèle selon le RMSE",best_model["modele"])
    c2.metric("RMSE", f"{best_model["RMSE"]:.2f}")

    st.subheader("Valeurs réelles et prévisions")
    model_name= st.selectbox("Choisir un modèle", options=list(results.keys()))
    result = results[model_name]

    plot_df = pd.DataFrame({"Valeur réelle": result["y_test"].to_numpy(),
                            "Prévision": result["predictions"]})

    fig = px.line(
        plot_df,
        y=["Valeur réelle", "Prévision"],
        labels={"index": "Observation", "value": "Consommation (MW)", "variable": "Série"}
    )
    st.plotly_chart(fig, width="stretch")

    st.caption(
        "Le RMSE mesure l'erreur de prévision : plus il est faible, mieux c'est. "
        "Le R² mesure la part de variabilité expliquée par le modèle."
    )
else:
    st.info("Clique sur « Entraîner les modèles » pour lancer la comparaison.")