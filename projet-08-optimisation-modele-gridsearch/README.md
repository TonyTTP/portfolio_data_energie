# Projet 08 — Optimisation de modèle avec GridSearchCV

## Objectif
Comparer régression linéaire et Random Forest sur une relation 
non-linéaire, puis optimiser les hyperparamètres du Random Forest 
avec GridSearchCV pour un modèle de prévision J+1.

## Ce que j'ai appris
- Pourquoi Random Forest capture mieux les relations non-linéaires 
  qu'une régression linéaire
- Cross-validation : comparaison R² train / test / cross-val pour 
  détecter l'overfitting
- GridSearchCV : recherche des meilleurs hyperparamètres 
  (`n_estimators`, `max_depth`, `min_samples_split`)
- Split temporel appliqué correctement (train = période passée, 
  test = période récente)
- Dashboard complet : réel vs prédit, feature importance, distribution 
  des erreurs, erreur par heure

## Technos utilisées
Python, Pandas, NumPy, scikit-learn (RandomForestRegressor, GridSearchCV), 
SQLite, Matplotlib
