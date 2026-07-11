# Projet 04 — Détection d'anomalies de consommation

## Objectif
Nettoyer un jeu de données de consommation électrique (valeurs manquantes), 
calculer des statistiques par région, et détecter les anomalies avec la 
méthode du Z-score (seuil à 2 écarts-types).

## Ce que j'ai appris
- Gestion des valeurs manquantes : `fillna()` avec la moyenne vs `ffill()` 
  selon le type de donnée
- Standardisation Z-score : `(valeur - moyenne) / écart-type`
- Stockage des résultats en SQLite et requêtage avec `strftime()` pour 
  grouper par mois
- Visualisation des anomalies sur une courbe temporelle avec matplotlib

## Technos utilisées
Python, Pandas, NumPy, SQLite, Matplotlib
