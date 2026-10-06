import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "data"))

from prophet import Prophet
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from fetch_rte import fetch_eco2mix
from clean import clean_rte

def train(df,periods=96):
    df_prophet = df.rename(columns={"date_heure" : "ds", "consommation" : "y"})[["ds","y"]].dropna()
    df_prophet["ds"] = df_prophet["ds"].dt.tz_localize(None)
    cutoff = df_prophet["ds"].quantile(0.8)
    df_train = df_prophet[df_prophet["ds"] <= cutoff]
    df_test = df_prophet[df_prophet["ds"] > cutoff]

    def nouveau_modele():
        return Prophet(
            yearly_seasonality=False,
            weekly_seasonality=True,
            daily_seasonality=True,
            seasonality_mode="multiplicative"
        )

    # Évaluation : entraînement sur 80 % des données, test sur les 20 % restants
    modele = nouveau_modele()
    modele.fit(df_train)
    forecast_test = modele.predict(df_test[["ds"]])
    df_eval = forecast_test.merge(df_test,on="ds",how="inner")

    # Prévision : ré-entraînement sur toutes les données pour prévoir après la dernière date connue
    modele = nouveau_modele()
    modele.fit(df_prophet)
    future = modele.make_future_dataframe(periods=periods,freq="15min")
    forecast = modele.predict(future)

    if len(df_eval) > 0:
        rmse = np.sqrt(mean_squared_error(df_eval["y"], df_eval["yhat"]))
        mape = np.mean(np.abs((df_eval["y"] - df_eval["yhat"]) / df_eval["y"])) *100
        print(f"RMSE = {rmse:.2f} MW")
        print(f"MAPE = {mape:.2f} %")
    else:
        rmse = None
        mape = None
    return rmse,mape,forecast,modele

if __name__ == "__main__":
    df_rte = fetch_eco2mix(days_back=90)
    if df_rte is not None:
        rmse, mape, forecast, modele = train(clean_rte(df_rte))
        print(forecast[["ds","yhat"]].tail())
