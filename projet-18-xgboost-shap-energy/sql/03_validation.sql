SELECT COUNT(*) AS total_lignes,
SUM(CASE WHEN temperature IS NULL THEN 1 ELSE 0 END) AS temperature_manquante,
SUM(CASE WHEN conso_mw IS NULL THEN 1 ELSE 0 END) AS consommation_manquante,
SUM(CASE WHEN conso_lag_48h IS NULL THEN 1 ELSE 0 END) AS lag_48h_manquant,
SUM(CASE WHEN conso_lag_7j IS NULL THEN 1 ELSE 0 END) AS lag_7j_manquant
FROM v_ml_features;

SELECT ROUND(AVG(conso_mw),2) AS conso_moyenne,
ROUND(MIN(conso_mw),2) AS conso_minimale,
ROUND(MAX(conso_mw),2) AS conso_maximale
FROM v_ml_features;

SELECT datetime, COUNT(*) AS nombre 
FROM eco2mix
GROUP BY datetime
HAVING COUNT(*) > 1;

SELECT datetime,conso_mw,temperature, conso_lag_48h,conso_lag_7j
FROM v_ml_features
ORDER BY datetime DESC
LIMIT 10;
