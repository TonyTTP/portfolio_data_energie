from pathlib import Path
import mlflow
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[2]

mlflow.set_tracking_uri(f"sqlite:///{(ROOT_DIR / 'mlflow.db').as_posix()}")

st.title("🧪 Suivi MLOps")
st.caption("Comparaison des expériences XGBoost avec MLflow")
experiment = mlflow.get_experiment_by_name("energy-forecast")
if experiment is None:
    st.warning("Aucune experience trouvée, lance experiments")
    st.stop()
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.rmse ASC"],)

if runs.empty:
    st.warning("Auncun run enregistré")
    st.stop()

columns = {

    "tags.mlflow.runName" : "Expérience",
    "metrics.rmse" : "RMSE",
    "metrics.r2" : "R²",
    "params.n_estimators" : "Nombre d'arbres",
    "params.learning_rate" : "Learning_rate",
}

available = {
    source: name
    for source, name in columns.items()
    if source in runs.columns
}

results = runs[list(available)].rename(columns=available)


if "RMSE" in results.columns:
    results["RMSE"] = pd.to_numeric(results["RMSE"], errors="coerce")
    valid = results.dropna(subset=["RMSE"])

    if not valid.empty:
        best = valid.iloc[0]

        col1, col2 = st.columns(2)
        col1.metric("Meilleur RMSE", f"{best['RMSE']:.2f}")

        if "R²" in valid.columns and pd.notna(best.get("R²")):
            col2.metric("Meilleur R²", f"{best['R²']:.4f}")

        st.subheader("Comparaison des modèles")

        if "Expérience" in valid.columns:
            fig = px.bar(
                valid,
                x="Expérience",
                y="RMSE",
                title="RMSE par expérience — plus bas = meilleur",
            )
            st.plotly_chart(fig, width="stretch")

st.subheader("Historique des runs")
st.dataframe(results, width="stretch")
