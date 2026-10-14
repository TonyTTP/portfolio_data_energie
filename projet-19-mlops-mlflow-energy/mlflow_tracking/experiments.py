import sys
from pathlib import Path
import mlflow
import mlflow.xgboost
import numpy as np
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "models"))
from train import load_data, FEATURES, TARGET

mlflow.set_tracking_uri(f"sqlite:///{(ROOT_DIR / 'mlflow.db').as_posix()}")
mlflow.set_experiment("energy-forecast")

def run_experiments():
    df = load_data()
    df = df.dropna(subset=list(FEATURES) + ["consommation"])
    df = df.copy()
    if len(df) < 50:
        raise ValueError(f"le nombre de lignes est trop peu : {len(df)}")
    X = df[list(FEATURES)]
    y = df["consommation"]
    split = int(len(df)*0.8)

    X_train, y_train = X.iloc[:split], y.iloc[:split]
    X_test,y_test = X.iloc[split:], y.iloc[split:]

    configurations = [{"n_estimators":100,"learning_rate":0.1,"max_depth":4},
                      {"n_estimators":300,"learning_rate":0.05,"max_depth":6},
                      {"n_estimators":500,"learning_rate":0.01,"max_depth":6}]

    for i, params in enumerate(configurations, start=1):

        with mlflow.start_run(run_name=f"xgb_config_{i}"):

            mlflow.log_params(params)
            mlflow.log_param("n_samples", len(df))
            mlflow.log_param("n_features", len(FEATURES))

            model = xgb.XGBRegressor(
                **params,
                objective="reg:squarederror",
                random_state=42,
                n_jobs=-1,)

            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            r2 = r2_score(y_test, predictions)

            mlflow.log_metric("rmse", float(rmse))
            mlflow.log_metric("r2", float(r2))
            mlflow.xgboost.log_model(model,name="model",input_example=X_train.head(3),)

            print(f"Configuration {i} | "f"RMSE : {rmse:.2f} | R² : {r2:.4f}")

if __name__ == "__main__":
    run_experiments()



    