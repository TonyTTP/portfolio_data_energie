from pathlib import Path 
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
from fetch_data import fetch_data
from clean import clean_data
from build_features import build_features

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

FEATURES = ["temperature","precipitation","irradiation","heure_sin","heure_cos","mois_sin","mois_cos","est_weekend",
            "est_hiver","conso_lag_48h","conso_lag_7j","conso_rolling_48h"]

def train_models():
    df = build_features(clean_data(fetch_data()))
    features = [col for col in FEATURES if col in df.columns]

    if not features:
        raise ValueError("Aucune variable explicative disponible")
    if "datetime" in df.columns:
        df = df.sort_values("datetime")
    df = df.dropna(subset=["conso_mw"])
    split = int(len(df)*0.8)

    train = df.iloc[:split]
    test = df.iloc[split:]

    X_train = train[features]
    y_train = train["conso_mw"]
    X_test = test[features]
    y_test = test["conso_mw"]

    models = {"random_forest" : 
              RandomForestRegressor(n_estimators=200, random_state=42,n_jobs=-1),
              "xgboost" : XGBRegressor(
            n_estimators=500,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            eval_metric="rmse",
            random_state=42,
            n_jobs=-1
                  
              )}

    results = {}

    for name, model in models.items():
        pipeline = Pipeline([("imputer", SimpleImputer(strategy="median")),("model", model)])

        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)

        rmse = mean_squared_error(y_test, predictions) ** 0.5
        r2 = r2_score(y_test, predictions)

        joblib.dump(pipeline,MODEL_DIR / f"{name}.joblib")

        results[name] = {
            "model": pipeline,
            "rmse": rmse,
            "r2": r2,
            "features": features,
            "X_test": X_test,
            "y_test": y_test,
            "predictions": predictions,
            "test_index": test.index
        }

        print(f"{name} | RMSE={rmse:.2f} MW | R²={r2:.3f}")

    best_name = min(results,key=lambda name: results[name]["rmse"])

    joblib.dump({
            "model": results[best_name]["model"],
            "features": features,
            "name": best_name
        },
        MODEL_DIR / "best_model.joblib")

    print(f"Meilleur modèle : {best_name}")

    return results


if __name__ == "__main__":
    train_models()

