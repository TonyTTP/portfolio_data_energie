-- Table "conso_energie" :
-- datetime | region | conso_mw | temperature



WITH dataset AS (SELECT datetime,region,conso_mw,temperature,
-- Variables temporelles
CAST(strftime('%H', datetime) AS INTEGER) AS heure,
CAST(strftime('%d', datetime) AS INTEGER) AS jour,
CAST(strftime('%m', datetime) AS INTEGER) AS mois,

-- Consommation 24h auparavant
LAG(conso_mw, 24) OVER (PARTITION BY region ORDER BY datetime ) AS conso_lag_24,

-- Moyenne mobile sur les 7 derniers jours
AVG(conso_mw) OVER (PARTITION BY region ORDER BY datetime
ROWS BETWEEN 167 PRECEDING AND CURRENT ROW ) AS moyenne_mobile_7j
FROM conso_energie
)
SELECT * FROM dataset WHERE conso_lag_24 IS NOT NULL;