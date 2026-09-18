--Requête 1 — Vue d'ensemble des données

SELECT COUNT(*) AS nbre_mesures,
MIN(datetime) AS premiere_valeur,
MAX(datetime) AS derniere_valeur,
ROUND(AVG(conso_mw),2) AS moyenne_conso,
ROUND(MAX(conso_mw),2) AS max_conso,
ROUND(MIN(conso_mw),2) AS min_conso,
FROM eco2mix;


--Requête 2 — Consommation par heure

SELECT CAST(strftime('%H',datetime) AS INT) AS heure
ROUND(AVG(conso_mw),2) AS conso_moy
ROUND(MAX(conso_mw),2) AS conso_max
ROUND(AVG(conso_mw),2) AS conso_moy
GROUP BY heure;
ORDER BY heure,


