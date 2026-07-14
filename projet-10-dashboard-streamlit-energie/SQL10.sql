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