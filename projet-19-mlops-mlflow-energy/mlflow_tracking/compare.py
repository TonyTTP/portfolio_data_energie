from pathlib import Path 
import mlflow 
import pandas as pd 

ROOT_DIR = Path(__file__).resolve().parents[1]
mlflow.set_tracking_uri(f"sqlite:///{(ROOT_DIR / 'mlflow.db').as_posix()}")

def compare_runs(): 
    experiment = mlflow.get_experiment_by_name("energy-forecast")
    if experiment is None:
        print("Auncune expérience trouvée")
        return 
    runs = mlflow.search_runs(experiment_ids=[experiment.experiment_id],order_by=["metrics.rmse ASC"],)
    if runs.empty:
        print("Auncun run enregistré")
        return 
    columns = ["tags.mlflow.runName", "metrics.rmse", "metrics.r2", "params.n_estimators", 
               "params.learning_rate", "params.max_depth"]
    available = [col for col in columns if col in runs.columns]
    results = runs[available].copy()
    print(results.head(10).to_string(index=False))
    return results

if __name__ == "__main__":
    compare_runs()