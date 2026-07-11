# Projet 09 — Prévision avec Prophet et séries temporelles

## Objectif
Comprendre les concepts fondamentaux des séries temporelles (tendance, 
saisonnalité, stationnarité) puis construire un modèle de prévision 
avec Prophet, incluant un régresseur externe (température).

## Ce que j'ai appris
- Décomposition d'une série temporelle : tendance, saisonnalité, résidus
- Stationnarité et différenciation (`.diff()`) pour stabiliser une série
- Prophet : format `ds`/`y`, ajout d'un régresseur externe avec 
  `add_regressor()`, intervalle de confiance
- Évaluation correcte sur un vrai holdout (jamais random pour du temporel)
- MAPE comme métrique interprétable en % d'erreur, avec des seuils de 
  référence sectoriels (RTE vise ~2% en J+1)
- Comparaison Prophet vs Random Forest sur les mêmes données

## Technos utilisées
Python, Pandas, NumPy, Prophet, scikit-learn, SQLite, Matplotlib
