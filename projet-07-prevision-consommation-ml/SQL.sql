

SELECT *FROM ( SELECT datetime, conso_mw, temperature,region,
        CAST(strftime('%H', datetime) AS INTEGER) AS heure,
        CAST(strftime('%d', datetime) AS INTEGER) AS jour,
        CAST(strftime('%m', datetime) AS INTEGER) AS mois,
        AVG(conso_mw) OVER (PARTITION BY strftime('%H', datetime)) AS conso_moyenne_heure,

        -- Consommation 24 h auparavant
        LAG(conso_mw, 24) OVER ( ORDER BY datetime) AS conso_lag_24
    FROM conso_rte
)
WHERE conso_lag_24 IS NOT NULL;