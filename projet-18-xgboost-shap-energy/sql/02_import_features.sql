DROP VIEW IF EXISTS v_ml_features;
CREATE VIEW IF NOT EXISTS v_ml_features AS
    WITH base AS(
        SELECT e.datetime, e.consommation AS conso_mw,
        CAST(strftime('%H',e.datetime) AS INTEGER) AS heure,
        CAST(strftime('%m',e.datetime) AS INTEGER) AS mois,
        CASE WHEN CAST(strftime('%w',e.datetime) AS INTEGER) IN (0,6) THEN 1
        ELSE 0 END AS est_weekend,

        CASE WHEN CAST(strftime('%m',e.datetime) AS INTEGER) IN (12,1,2) THEN 1 ELSE 0 END AS est_hiver,

        m.temperature, m.precipitation, m.irradiation, m.vitesse_vent, m.humidity, m.pression_atm,
        
        LAG(e.consommation,48) OVER (ORDER BY e.datetime) AS conso_lag_48h,
        LAG(e.consommation,168) OVER (ORDER BY e.datetime)AS conso_lag_7j,
        AVG(e.consommation) OVER (ORDER BY e.datetime ROWS BETWEEN 48 PRECEDING AND 1 PRECEDING
        ) AS conso_rolling_48h

    FROM eco2mix e
    LEFT JOIN meteo m 
        ON e.datetime = m.time
        AND m.ville = 'Paris'
    WHERE e.consommation IS NOT NULL
)
SELECT *FROM base;



    
