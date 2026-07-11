# Projet 02 — Agrégations SQL sur données de production énergie

## Objectif
Manipuler une table de production électrique par centrale (type de source, 
région) avec des requêtes d'agrégation : somme par type d'énergie, moyenne 
par région avec filtrage sur l'agrégat.

## Ce que j'ai appris
- `GROUP BY` combiné à `SUM()` pour totaliser une production par catégorie
- `HAVING` appliqué correctement sur une fonction d'agrégation 
  (`AVG(production_mw) > 500`) plutôt que sur la colonne brute
- `COUNT()` pour dénombrer les lignes par groupe en complément de la moyenne
- Tri des résultats agrégés avec `ORDER BY` sur une fonction d'agrégation

## Technos utilisées
SQL, SQLite
