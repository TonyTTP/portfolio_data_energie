# Projet 06 — Dashboard mix énergétique façon RTE

## Objectif
Analyser un an de données horaires de consommation et de production 
(nucléaire, éolien, solaire) : mix énergétique, courbe de charge, 
détection de pics de consommation par Z-score.

## Ce que j'ai appris
- Génération de données horaires réalistes avec saisonnalité (sin/cos)
- Feature engineering temporel : heure, jour, mois, saison, weekend
- Calcul de parts en pourcentage (mix énergétique) et agrégation mensuelle
- Dashboard 2x2 avec courbe de charge, camembert, barres et scatter
- Rapport texte automatique généré depuis les résultats calculés

## Technos utilisées
Python, Pandas, NumPy, SQLite, Matplotlib
