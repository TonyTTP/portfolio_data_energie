import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)


dates = pd.date_range("2022-01-01", periods=730, freq="D")


tendance    = np.linspace(45000, 48000, 730)
saisonnalite = 8000 * np.cos(
               np.linspace(0, 4*np.pi, 730)
               )
bruit        = np.random.normal(0, 1000, 730)

df = pd.DataFrame({
    "date"    : dates,
    "conso_mw": tendance + saisonnalite + bruit
})
df = df.set_index("date")

print("===== Définitions =====")
print("- Une tendance représente l'évolution générale de la série dans le temps.")
print("- La saisonnalité correspond à un phénomène qui se répète régulièrement.")
print("- Les résidus sont la différence entre les observations et la tendance.")
print()



plt.plot(df.index, df["conso_mw"])
plt.show()



df["mm_30"] = df["conso_mw"].rolling(window=30).mean()

df["conso_mw"].plot(figsize=(6,6), color="blue", label="Conso")
df["mm_30"].plot(color="orange", label="Moyenne mobile")
plt.title("Conso vs Moyenne mobile 30 jours")
plt.legend()
plt.show()




df["trend"] = df["conso_mw"].rolling(window=90).mean()
df["saison"] = df["conso_mw"].rolling(window=7).mean()
df["residus"] = df["conso_mw"] - df["trend"]

fig, axes = plt.subplots(3,1, figsize=(6,6))

df["trend"].plot(ax=axes[0], title="Tendance", color="blue")
df["saison"].plot(ax=axes[1], title="Saisonnalité", color="orange")
df["residus"].plot(ax=axes[2], title="Résidus", color="green")

plt.tight_layout()
plt.show()





plt.figure(figsize=(14,5))
df["conso_mw"].plot(title="Test visuel de stationnarité")
plt.show()


df["conso_diff"] = df["conso_mw"].diff(1)



fig,axes = plt.subplots(2,1, figsize=(6,6))

df["conso_mw"].plot(ax=axes[0], title="Consommation", color="green")
df["conso_diff"].plot(ax=axes[1], title="Différence d'un jour à l'autre", color="red")
plt.tight_layout()
plt.legend()
plt.show()



# pip install prophet
from prophet import Prophet
from sklearn.metrics import mean_squared_error



df_prophet = df.reset_index().rename(columns={"date": "ds", "conso_mw": "y"})

# 1. Entraîne le modèle

model = Prophet(
    yearly_seasonality=True,   
    weekly_seasonality=True, 
    daily_seasonality=False  
                            
)

model.fit(df_prophet)



future = model.make_future_dataframe(periods=90)



forecast = model.predict(future)



model.plot(forecast)
plt.title("Prévision de la consommation électrique avec Prophet")
plt.xlabel("Date")
plt.ylabel("Conso")
plt.legend()
plt.show()


model.plot_components(forecast)
plt.show()

train = df_prophet.iloc[:-90]


test = df_prophet.iloc[-90:]



model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

model.fit(train)



future = model.make_future_dataframe(periods=90)

forecast = model.predict(future)


y_pred = forecast["yhat"].tail(90).values
y_test = test["y"].values

# RMSE

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print(f"RMSE : {rmse:.2f} MW")

# MAPE

mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

print(f"MAPE : {mape:.2f}%")



# 1. Split correct :
n = len(df)
train_size = int(n * 0.8)

df_train = df.iloc[:train_size]   # 80% début
df_test  = df.iloc[train_size:]   # 20% fin






train = df_train.reset_index().rename(
    columns={"date": "ds", "conso_mw": "y"}
)

test = df_test.reset_index().rename(
    columns={"date": "ds", "conso_mw": "y"}
)

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False
)

model.fit(train)



future = model.make_future_dataframe(periods=len(test),freq="D")

forecast = model.predict(future)



y_test = test["y"].values
y_pred = forecast["yhat"].tail(len(test)).values

# Calcul des métriques


from sklearn.metrics import (mean_squared_error,r2_score)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))

mape = np.mean(np.abs((y_test-y_pred)/y_test)) * 100

r2 = r2_score(y_test,y_pred)

print(f"RMSE : {rmse:.2f} MW")
print(f"MAPE : {mape:.2f}%")
print(f"R²   : {r2:.3f}")



plt.figure(figsize=(15,5))
plt.plot(df_test.index,y_test,label="Réel")
plt.plot(df_test.index,y_pred,label="Prédit")

plt.fill_between(df_test.index,forecast["yhat_lower"].tail(len(test)), forecast["yhat_upper"].tail(len(test)),
    alpha=0.3,
    label="Intervalle de confiance"
)

plt.title("Prévisions Prophet")
plt.xlabel("Date")
plt.ylabel("Consommation (MW)")
plt.legend()
plt.grid(True)
plt.show()

# Projet : Système de prévision
# consommation électrique façon RTE

import pandas as pd
import numpy as np
from prophet import Prophet
from sklearn.metrics import (
    mean_squared_error,
    r2_score
)
import matplotlib.pyplot as plt
import sqlite3



dates = pd.date_range("2021-01-01",periods=1095,freq="D")

np.random.seed(42)



tendance = np.linspace(45000,47000,1095)
saison_annee = 8000 * np.cos(np.linspace(0, 6*np.pi, 1095))
saison_semaine = 2000 * np.sin(np.linspace(0, 2*np.pi*156, 1095))
bruit = np.random.normal(0,800,1095)

df = pd.DataFrame({
    "ds": dates,
    "y": tendance + saison_annee + saison_semaine + bruit,
    "temp": 10 + 12*np.cos(np.linspace(0,6*np.pi,1095)) + np.random.normal(0,3,1095)})


model = Prophet()
model.add_regressor("temp")



train = df.iloc[:730]
test = df.iloc[730:]



model.fit(train)
future = test[["ds","temp"]]
forecast = model.predict(future)



y_test = test["y"]
y_pred = forecast["yhat"]
rmse = np.sqrt(mean_squared_error(y_test,y_pred))
mape = np.mean(np.abs((y_test.values - y_pred.values) / y_test.values)) * 100
r2 = r2_score(y_test,y_pred)

print(f"RMSE : {rmse:.2f} MW")
print(f"MAPE : {mape:.2f}%")
print(f"R² : {r2:.3f}")



conn = sqlite3.connect("previsions_energie.db")

previsions = pd.DataFrame({"date": test["ds"],"reel": y_test,"predit": y_pred,
"lower": forecast["yhat_lower"],
"upper": forecast["yhat_upper"]

})

previsions.to_sql("previsions_prophet",conn,if_exists="replace",index=False)
metriques = pd.DataFrame({"rmse":[rmse],"mape":[mape],"r2":[r2],"date_evaluation":[pd.Timestamp.today()]
})

metriques.to_sql("metriques",conn,if_exists="replace",index=False)
conn.close()

Dashboard final

fig, axes = plt.subplots(2,2,figsize=(16,10))



axes[0,0].plot(train["ds"],train["y"],label="Train")
axes[0,0].plot(test["ds"],y_pred,label="Prévision")
axes[0,0].set_title("Série complète")
axes[0,0].legend()


axes[0,1].plot(test["ds"],y_test,label="Réel")
axes[0,1].plot(test["ds"],y_pred,label="Prédit")
axes[0,1].legend()
axes[0,1].set_title("Zoom période test")

axes[1,0].axis("off")
axes[1,0].text(0.5, 0.5,
    f"RMSE : {rmse:.0f} MW\nMAPE : {mape:.2f}%\nR² : {r2:.3f}",
    ha="center", va="center", fontsize=14, transform=axes[1,0].transAxes)
axes[1,0].set_title("Métriques")



erreurs = y_test.values - y_pred.values
axes[1,1].hist(erreurs,bins=30)
axes[1,1].set_title("Distribution des erreurs")
plt.tight_layout()
plt.show()



model.plot_components(forecast)
plt.show()





ic_moyen = np.mean(forecast["yhat_upper"]-forecast["yhat_lower"])/2

print(f"""========== PRÉVISION CONSO ÉLECTRIQUE ==========
Période train : 2021-2022
Période test  : 2023
RMSE : {rmse:.0f} MW
MAPE : {mape:.2f} %
R² : {r2:.3f}
{"✅ Bon modèle" if mape < 5 else "⚠️ À améliorer"}
Intervalle de confiance moyen :
±{ic_moyen:.0f} MW
===============================================
""")