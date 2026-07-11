# Projet 05 — Dashboard météo-énergie

## Objectif
Récupérer des données météo réelles via l'API publique Open-Meteo pour 
plusieurs villes françaises, croiser avec des données de consommation 
simulées, et identifier la corrélation température/consommation.

## Ce que j'ai appris
- Consommation d'API REST avec `requests` (paramètres, gestion des codes 
  de statut, parsing JSON)
- Fonction réutilisable pour récupérer les données de plusieurs villes 
  sans dupliquer le code
- CTE SQL (`WITH`) pour calculer la ville la plus froide par mois
- Sous-requête corrélée pour comparer une valeur à une moyenne globale
- Subplots matplotlib pour un dashboard multi-graphiques

## Technos utilisées
Python, Pandas, Requests, SQLite, Matplotlib, API Open-Meteo
