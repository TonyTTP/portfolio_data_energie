# Projet 07 — Prévision de consommation avec Machine Learning

## Objectif
Prévoir la consommation électrique à partir de features temporelles 
(régression linéaire puis Random Forest), avec feature engineering 
avancé (encodage cyclique, lags, moyenne mobile).

## Ce que j'ai appris
- Split train/test — et pourquoi il doit être **temporel** (pas aléatoire) 
  pour des séries chronologiques
- Encodage cyclique de l'heure avec sin/cos (23h est proche de 0h)
- Création de features de lag (`conso_lag_24`, `conso_lag_168`) pour 
  capturer la saisonnalité journalière et hebdomadaire
- Interprétation RMSE et R², feature importance d'un Random Forest
- Différence entre évaluer un modèle sur ses données d'entraînement 
  et sur un vrai jeu de test (piège que j'ai corrigé après coup)

## Technos utilisées
Python, Pandas, NumPy, scikit-learn (LinearRegression, RandomForestRegressor), 
SQLite, Matplotlib
