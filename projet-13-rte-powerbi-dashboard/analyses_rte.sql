--Requête 1 — Vue d'ensemble des données

SELECT COUNT(*) AS nbre_mesures,
    MIN(date_heure) AS premiere_valeur,
    MAX(date_heure) AS derniere_valeur,
    ROUND(AVG(consommation_brute_totale),2) AS moyenne_conso,
    ROUND(MAX(consommation_brute_totale),2) AS max_conso,
    ROUND(MIN(consommation_brute_totale),2) AS min_conso
FROM eco_mix;


--Requête 2 — Consommation par heure

SELECT CAST(strftime('%H',date_heure) AS INT) AS heure,
    ROUND(AVG(consommation_brute_totale),2) AS conso_moy,
    ROUND(MAX(consommation_brute_totale),2) AS conso_max,
    ROUND(MIN(consommation_brute_totale),2) AS conso_min
FROM eco_mix
GROUP BY heure
ORDER BY heure;


--Requête 3 — Consommation par saison

SELECT
    CASE
        WHEN CAST(strftime('%m',date_heure) AS INT) IN (12,1,2) THEN 'Hiver'
        WHEN CAST(strftime('%m',date_heure) AS INT) IN (3,4,5) THEN 'Printemps'
        WHEN CAST(strftime('%m',date_heure) AS INT) IN (6,7,8) THEN 'Ete'
        ELSE 'Automne'
    END AS saison,
    ROUND(AVG(consommation_brute_totale),2) AS conso_moy,
    COUNT(*) AS nbre_mesure
FROM eco_mix
GROUP BY saison
ORDER BY conso_moy DESC;


-- Requête 4 — Semaine vs week-end

SELECT CASE WHEN CAST(strftime('%w',date_heure) AS INT) IN (1,2,3,4,5) THEN 'jour_semaine'
    ELSE 'weekend' END AS type_jour,
    ROUND(AVG(consommation_brute_totale),2) AS conso_moy,
    COUNT(*) AS nbre_mesure
FROM eco_mix
GROUP BY type_jour
ORDER BY conso_moy DESC;