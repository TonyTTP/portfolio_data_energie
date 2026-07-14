-- (métriques)
--Consommation moyenne, Pic max année, Pic maximum sur l'année
-- min sur l'année, écart entre max et min

SELECT ROUND(AVG(conso_mw),0) AS moy_conso, ROUND(MAX(conso_mw),0) AS max_conso,
ROUND(MIN(conso_mw),0) AS conso_min, ROUND(MAX(conso_mw) - MIN(conso_mw),0) AS ecart
FROM conso_journaliere
ORDER BY region;

-- Récupère toutes les régions disponibles

SELECT region 
FROM conso_journaliere
ORDER BY region;

-- on va remplacer 'Paris' par le choix utilisateur

SELECT date,region,ROUND(conso_mw,0) AS conso,ROUND(prod_nucleaire,0) AS prod_nucleaire,
ROUND(prod_eolien,0) AS prod_eolien, ROUND(temperature,1) AS temperature
FROM conso_journaliere
WHERE region = 'Paris'
ORDER BY region;

--Moyenne mobile 7 jours

SELECT date,region,ROUND(AVG(conso_mw) OVER(PARTITION BY region ORDER BY date
ROWS BETWEEN 6 AND PRECEDING CURRENT ROW),0) AS moyenne_mobile
FROM conso_journaliere
WHERE region = 'Paris'
ORDER BY region;

-- REQUÊTE 6 — Corrélation température/conso
SELECT date, region ROUND(temperature,0) AS temperature ROUND(conso_mw,0) AS consommation
FROM conso_journaliere 
WHERE region = 'Paris' AND temperature IS NOT NULL AND conso_mw IS NOT NULL
ORDER BY region;

-- REQUÊTE 7 — Comparaison régions
-- (tableau comparatif dans l'app)

SELECT region, ROUND(AVG(conso_mw),0) AS conso_moy, ROUND(temperature,0) AS temperature,
ROUND(MAX(conso_mw),0) AS conso_max, ROUND(MIN(conso_mw),0) AS conso_min,
COUNT(*) AS nb_jours
FROM conso_journaliere
GROUP BY region
ORDER AVG(conso_mw) DESC;

--Top 5 jours de pointe avec le plus de conso

SELECT region,date, ROUND(conso_mw,0) AS conso
FROM conso_journaliere

ORDER BY ROUND(conso_mw,0) DESC LIMIT 5;

-- Évolution mensuelle


SELECT strftime('%Y-%m') AS mois, AVG(conso_mw) AS conso_moy, AVG(temperature) AS temp_moy, 
SUM(prod_eolien) AS moy_eolien,
SUM(prod_nucleaire) AS somme_mucleaire,
region, date,
FROM conso_journaliere
GROUP BY mois,region
ORDER BY mois,region;

-- Sous-requête pour calculer moyenne + écart-type
-- Puis filtre les valeurs > moyenne + 2*std

SELECT date,region,ROUND(conso_mw, 0)  AS conso_mw,
ROUND(stats.moy, 0) AS conso_moyenne,ROUND(stats.std, 0) AS ecart_type
FROM conso_journaliere
JOIN ( SELECT region, AVG(conso_mw) AS moy, 
AVG((conso_mw - AVG(conso_mw)) * (conso_mw - AVG(conso_mw))) AS std
FROM conso_journaliere
GROUP BY region
) AS stats USING (region)
WHERE conso_mw > stats.moy + 2 * stats.std
ORDER BY conso_mw DESC;