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


--Requête 3 — Consommation par saison

SELECT CASE WHEN(CAST(strftime('%m',datetime) AS INT) IN [12,1,2] THEN 'Hiver')
SELECT CASE WHEN(CAST(strftime('%m',datetime) AS INT) IN [3,4,5] THEN 'Printemps')
SELECT CASE WHEN(CAST(strftime('%m',datetime) AS INT) IN [6,7,8] THEN 'Ete')
ELSE 'Automne' END AS saison,
ROUND(AVG(conso_mw),2) AS conso_moy
COUNT(*) AS nbre_mesure
FROM eco2mix
GROUP BY saison
ORDER BY conso_moy DESC;


-- Requête 4 — Semaine vs week-end


SELECT CASE WHEN CAST(strftime('%w',datetime) AS INT) IN (1,2,3,4,5) THEN 'jour_semaine'
ELSE 'weekend' END AS type_jour,
ROUND(AVG(conso_mw),2) AS conso_moy,
COUNT(*) AS nbre_mesure
FROM eco2mix
GROUP BY type_jour
ORDER BY conso_moy DESC;







