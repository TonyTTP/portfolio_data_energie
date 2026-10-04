CREATE VIEW IF NOT EXISTS v_dashboard AS
SELECT e.date_heure, e.consommation, e.solaire,e.eolien,e.hydraulique,e.nucleaire,e.taux_co2,
ROUND((e.solaire + e.eolien + e.hydraulique) * 100.0 / e.consommation,1) AS part_renouv_pct,
m.ville, m.precipitation,m.temperature_2m
FROM eco2mix AS e
LEFT JOIN meteo AS m
ON SUBSTR(e.date_heure,1,13) = SUBSTR(m.time,1,13)
AND m.ville = 'Paris'
WHERE e.consommation IS NOT NULL;

CREATE VIEW IF NOT EXISTS v_kpi AS
SELECT ROUND(AVG(consommation),1) AS moy_conso,
ROUND(AVG(taux_co2),1) AS moy_co2,
ROUND(AVG(part_renouv_pct),1) AS part_moy_renouv_pct,
ROUND(MAX(consommation),1) AS max_conso,
ROUND(MIN(consommation),1) AS min_conso
FROM v_dashboard;

SELECT * FROM v_dashboard;
