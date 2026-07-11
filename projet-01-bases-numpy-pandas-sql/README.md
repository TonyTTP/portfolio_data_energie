# Projet 01 — Bases NumPy, Pandas & SQL

## Objectif
Premiers pas avec la manipulation de données de consommation électrique : 
arrays NumPy, DataFrames Pandas, et stockage/requêtage en base SQLite.

## Ce que j'ai appris
- Manipulation d'arrays NumPy : indexation, `.mean()`, `.max()`, `.std()`
- Création de DataFrames Pandas et calcul de colonnes dérivées 
  (ex : consommation totale = matin + soir)
- Stockage d'un DataFrame en base SQLite avec `to_sql()`
- Requêtage SQL depuis Python avec `pd.read_sql()`
- `GROUP BY` avec agrégation (`AVG`) et filtrage avec `HAVING`
- Différence importante entre filtrer sur une colonne brute et filtrer 
  sur un résultat agrégé (piège classique du `HAVING`)

## Technos utilisées
Python, NumPy, Pandas, SQLite
