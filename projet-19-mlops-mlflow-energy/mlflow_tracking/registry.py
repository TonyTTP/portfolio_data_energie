from pathlib import Path 
from mlflow import mlflow, MlflowClient
import pandas as pd
ROOT_DIR = Path(__file__).resolve().parents[1]
mlflow.set_tracking_uri(f"sqlite:///{(ROOT_DIR / 'mlflow.db').as_posix()}")
client = MlflowClient()

def register_best_model():
    experiment = mlflow.get_experiment_by_name("energy-forecast")
    if experiment is None:
        raise ValueError("Experience energy-forecast introuvable")
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string="attributes.status = 'FINISHED'",
        order_by=["metrics.rmse ASC"],
        max_results=1,)

    if runs.empty or pd.isna(runs.iloc[0]["metrics.rmse"]):
        raise ValueError("Aucun run terminé avec une métrique RMSE disponible ")
    best_run = runs.iloc[0]
    run_id = best_run["run_id"]

    model_uri = f"runs:/{run_id}/model"

    registered_model = mlflow.register_model(
        model_uri=model_uri,
        name="energy-forecast-xgb",
    )

    print("Meilleur modèle enregistré.")
    print(f"Run ID : {run_id}")
    print(f"RMSE : {best_run['metrics.rmse']:.2f}")
    print(f"Version : {registered_model.version}")

    return registered_model

if __name__ == "__main__":
    register_best_model()
