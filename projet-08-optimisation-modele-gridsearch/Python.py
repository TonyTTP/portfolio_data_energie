import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

np.random.seed(42)
n = 2000

df = pd.DataFrame({
    "temperature"  : np.random.randint(-5, 35, n),
    "heure"        : np.random.randint(0, 24, n),
    "jour_semaine" : np.random.randint(0, 7, n),
    "mois"         : np.random.randint(1, 13, n),
})

# Relation NON-LINÉAIRE avec la conso
df["conso_mw"] = (
    50000
    - 500  * df["temperature"]
    + 200  * df["temperature"]**2  # ← non linéaire !
    + 3000 * np.sin(df["heure"] * np.pi / 12)
    + np.random.normal(0, 1500, n)
)

X = df.drop("conso_mw", axis=1)
y = df["conso_mw"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)



lin = LinearRegression()
lin.fit(X_train, y_train)

pred_lr = lin.predict(X_test)

rmse_lr = np.sqrt(mean_squared_error(y_test, pred_lr))
r2_lr = r2_score(y_test, pred_lr)

print("=== Régression Linéaire ===")
print("RMSE:", rmse_lr)
print("R²:", r2_lr)




rf = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

rf.fit(X_train, y_train)

pred_rf = rf.predict(X_test)

rmse_rf = np.sqrt(mean_squared_error(y_test, pred_rf))
r2_rf = r2_score(y_test, pred_rf)

print("\n=== Random Forest ===")
print("RMSE:", rmse_rf)
print("R²:", r2_rf)




print("\n=== COMPARAISON ===")
print(f"Linéaire R²  : {r2_lr:.3f}")
print(f"RF R²        : {r2_rf:.3f}")



importances = pd.DataFrame({
    "feature": X.columns,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False)

print("\nFeature importance:")
print(importances)


import matplotlib.pyplot as plt

plt.figure(figsize=(6,4))
plt.barh(importances["feature"], importances["importance"])
plt.gca().invert_yaxis()
plt.title("Feature Importance - Random Forest")
plt.show()





from sklearn.model_selection import cross_val_score



cv_scores = cross_val_score(
    rf, X, y,
    cv=5,
    scoring="r2"
)



print("\n=== CROSS VALIDATION ===")
print("Scores:", cv_scores)
print("Mean:", cv_scores.mean())
print("Std:", cv_scores.std())



print("\nTrain R²:", rf.score(X_train, y_train))
print("Test R²:", rf.score(X_test, y_test))
print("CV mean:", cv_scores.mean())


from sklearn.model_selection import GridSearchCV


param_grid = {
    "n_estimators" : [50, 100, 200],
    "max_depth"    : [5, 10, None],
    "min_samples_split" : [2, 5, 10]
}


grid_search = GridSearchCV(RandomForestRegressor(random_state=42),param_grid,
    cv=3,scoring='r2',n_jobs=-1  # utilise tous les CPU
)

grid_search.fit(X_train, y_train)


print("\nBest params:", grid_search.best_params_)


best_model = grid_search.best_estimator_

pred_best = best_model.predict(X_test)

rmse_best = np.sqrt(mean_squared_error(y_test, pred_best))
r2_best = r2_score(y_test, pred_best)

print("Best model R²:", r2_best)



import matplotlib.pyplot as plt
import sqlite3

# Étape 1 : Données + Feature Engineering
dates = pd.date_range("2021-01-01", periods=2000, freq="h")
np.random.seed(42)

df = pd.DataFrame({"datetime": dates})

df["temperature"] = (
    10 + 15 * np.sin(np.linspace(0, 6*np.pi, len(df)))
    + np.random.normal(0, 3, len(df))
)

df["conso_mw"] = (
    50000
    - 500  * df["temperature"]
    + 3000 * np.sin(df["datetime"].dt.hour * np.pi / 12)
    + np.random.normal(0, 2000, len(df))
)


df["heure"] = df["datetime"].dt.hour
df["jour"] = df["datetime"].dt.dayofweek
df["mois"] = df["datetime"].dt.month
df["est_weekend"] = (df["jour"] >= 5).astype(int)

df["heure_sin"] = np.sin(2 * np.pi * df["heure"] / 24)
df["heure_cos"] = np.cos(2 * np.pi * df["heure"] / 24)

df["conso_lag_24"] = df["conso_mw"].shift(24)
df["conso_lag_168"] = df["conso_mw"].shift(168)

df = df.dropna()



split = int(len(df) * 0.8)

train = df.iloc[:split]
test = df.iloc[split:]

features = [
    "temperature", "heure", "jour", "mois", "est_weekend",
    "heure_sin", "heure_cos",
    "conso_lag_24", "conso_lag_168"
]

X_train = train[features]
y_train = train["conso_mw"]

X_test = test[features]
y_test = test["conso_mw"]


grid_search.fit(X_train, y_train)

best_model = grid_search.best_estimator_


pred = best_model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, pred))
r2 = r2_score(y_test, pred)



y_pred = best_model.predict(X_test)   


conn = sqlite3.connect("energy_model.db")

df_predictions = pd.DataFrame({
    "datetime": test["datetime"],  
    "conso_reelle": y_test,
    "conso_predite": y_pred
})
df_predictions["erreur"] = df_predictions["conso_reelle"] - df_predictions["conso_predite"]

df_predictions.to_sql("predictions_j1", conn, if_exists="replace", index=False)

df_importance = pd.DataFrame({
    "variable": features,
    "importance": best_model.feature_importances_
}).sort_values("importance", ascending=False)

df_importance.to_sql("feature_importance", conn, if_exists="replace", index=False)

conn.close()


fig, axes = plt.subplots(2, 2, figsize=(15,10))

axes[0,0].plot(y_test.values[-168:], label="Réel")
axes[0,0].plot(pred[-168:], label="Prédit")
axes[0,0].set_title("7 derniers jours")
axes[0,0].legend()



axes[0,1].barh(df_importance["variable"], df_importance["importance"])
axes[0,1].set_title("Feature importance")

axes[1,0].hist(y_test - pred, bins=30)
axes[1,0].set_title("Erreurs")

axes[1,1].scatter(test["heure"], np.abs(y_test - pred), alpha=0.3)
axes[1,1].set_title("Erreur par heure")

plt.tight_layout()
plt.show()


cv_scores = cross_val_score(best_model, X_train, y_train, cv=3, scoring="r2")

top_feature = df_importance.iloc[0]["variable"]
print(f"""
=== MODÈLE PRÉVISION J+1 ===
Meilleurs paramètres : {grid_search.best_params_}
R² test    : {r2:.3f}
RMSE test  : {rmse:.0f} MW
R² cross-val : {cv_scores.mean():.3f} ± {cv_scores.std():.3f}
Feature la plus importante : {top_feature}
""")