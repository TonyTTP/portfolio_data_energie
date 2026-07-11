
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

# Données simulées façon RTE
np.random.seed(42)
n = 1000

temperature = np.random.randint(-5, 35, n)
heure = np.random.randint(0, 24, n)
jour_semaine = np.random.randint(0, 7, n)
mois = np.random.randint(1, 13, n)

conso_mw = (
    50000
    - 500 * temperature
    + 1000 * np.sin(heure * np.pi / 12)
    + np.random.normal(0, 2000, n)
)

df = pd.DataFrame({
    "temperature": temperature,
    "heure": heure,
    "jour_semaine": jour_semaine,
    "mois": mois,
    "conso_mw": conso_mw
})


print(df.info())
print(df.corr()["conso_mw"])
X = df.drop(columns="conso_mw")
y = df["conso_mw"]
print(X.shape)
print(y.shape)


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("X_train :", X_train.shape)
print("X_test  :", X_test.shape)
print("y_train :", y_train.shape)
print("y_test  :", y_test.shape)


model = LinearRegression()
model.fit(X_train, y_train)




y_pred = model.predict(X_test)



rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE : {rmse:.2f} MW")
print(f"R² : {r2:.3f}")




coefficients = pd.DataFrame({
    "feature": X.columns,
    "coefficient": model.coef_
}).sort_values(by="coefficient")

print(coefficients)



df["heure_sin"] = np.sin(2 * np.pi * df["heure"] / 24)
df["heure_cos"] = np.cos(2 * np.pi * df["heure"] / 24)

df["est_weekend"] = (df["jour_semaine"] >= 5).astype(int)
df["est_hiver"] = df["mois"].isin([12, 1, 2]).astype(int)

print(df)



X = df.drop(columns="conso_mw")
y = df["conso_mw"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)


rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE : {rmse:.2f} MW")
print(f"R² : {r2:.3f}")



plt.figure(figsize=(6, 6))

plt.scatter(y_test, y_pred, alpha=0.5)

plt.plot(
    [y_test.min(), y_test.max()],
    [y_test.min(), y_test.max()],
    "r--"
)

plt.xlabel("Réel")
plt.ylabel("Prédit")
plt.title("Consommation réelle vs prédite")

plt.show()

# Projet : Prévoir la consommation électrique J+1


import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import sqlite3


dates = pd.date_range("2022-01-01",
                       periods=17520, freq="h")
np.random.seed(42)

df = pd.DataFrame({"datetime": dates})
df["temperature"]  = 10 + 15*np.sin(
                     np.linspace(0, 4*np.pi, len(df))
                     ) + np.random.normal(0, 3, len(df))
df["conso_mw"]     = (50000
                     - 500 * df["temperature"]
                     + np.random.normal(0, 2000, len(df)))


df["heure"] = df["datetime"].dt.hour
df["jour"] = df["datetime"].dt.dayofweek
df["mois"] = df["datetime"].dt.month


df["est_weekend"] = (df["jour"] >= 5).astype(int)
df["est_hiver"] = df["mois"].isin([12, 1, 2]).astype(int)


df["heure_sin"] = np.sin(2 * np.pi * df["heure"] / 24)
df["heure_cos"] = np.cos(2 * np.pi * df["heure"] / 24)


df["conso_lag_24"] = df["conso_mw"].shift(24)


df["conso_lag_168"] = df["conso_mw"].shift(168)


df["temp_rolling_24"] = (
    df["temperature"]
    .rolling(window=24)
    .mean()
)


df = df.dropna().reset_index(drop=True)



X = df.drop(columns=["datetime", "conso_mw"])
y = df["conso_mw"]


split_idx = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]


model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


model.fit(X_train, y_train)

scores = cross_val_score(
    model,
    X,
    y,
    cv=5,
    scoring="r2"
)

print("Scores R² :", scores)
print(f"R² moyen : {scores.mean():.3f}")



feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

print(feature_importance)


y_pred = model.predict(X)


predictions = pd.DataFrame({
    "datetime": df["datetime"],
    "reel": y,
    "predit": y_pred
})


conn = sqlite3.connect("rte_predictions.db")


predictions.to_sql(
    "predictions",
    conn,
    if_exists="replace",
    index=False
)

feature_importance.to_sql(
    "feature_importance",
    conn,
    if_exists="replace",
    index=False
)


conn.close()




residus = y - y_pred


plt.figure(figsize=(10, 5))
plt.plot(df["datetime"], y, label="Réel")
plt.plot(df["datetime"], y_pred, label="Prédit")
plt.title("Consommation réelle vs prédite")
plt.xlabel("Date")
plt.ylabel("Consommation (MW)")
plt.legend()
plt.show()


plt.figure(figsize=(10, 5))
plt.plot(df["datetime"], residus)
plt.title("Résidus (erreurs de prédiction)")
plt.xlabel("Date")
plt.ylabel("Erreur (MW)")
plt.axhline(0, color="red", linestyle="--")
plt.show()


plt.figure(figsize=(8, 6))
plt.barh(
    feature_importance["feature"],
    feature_importance["importance"]
)
plt.title("Importance des variables")
plt.xlabel("Importance")
plt.gca().invert_yaxis()
plt.show()

plt.figure(figsize=(8, 5))
plt.hist(residus, bins=30)
plt.title("Distribution des erreurs")
plt.xlabel("Erreur (MW)")
plt.ylabel("Fréquence")
plt.show()