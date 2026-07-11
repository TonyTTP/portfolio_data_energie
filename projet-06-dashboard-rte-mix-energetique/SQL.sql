-- ============================================
-- EXERCICE 3 - Requêtes basiques
-- ============================================

-- Requête 1 : Conso moyenne par région
SELECT region, AVG(conso_mw) AS conso_moy
FROM conso_horaire
GROUP BY region
HAVING AVG(conso_mw) > 46000
ORDER BY conso_moy DESC;


-- Requête 2 : Production nucléaire moyenne par mois d'hiver
SELECT mois, AVG(prod_nucleaire) AS nuc_moy
FROM conso_horaire
WHERE mois IN (12, 1, 2)
GROUP BY mois
ORDER BY mois;


-- ============================================
-- EXERCICE 5 - Pics de consommation
-- ============================================

-- Requête 3 : Top 10 jours avec le plus de pics
SELECT strftime('%Y-%m-%d', datetime) AS jour,
       COUNT(*) AS nb_pics
FROM pics_conso
GROUP BY jour
ORDER BY nb_pics DESC
LIMIT 10;


-- ============================================
-- EXERCICE 6 - Dashboard complet
-- ============================================

-- Requête 4 : Courbe de charge moyenne par heure
SELECT heure, AVG(conso_mw) AS conso_moy
FROM conso_horaire
GROUP BY heure
ORDER BY heure;


-- Requête 5 : Mix énergétique par saison
SELECT saison,
       AVG(prod_nucleaire) AS nuc_moy,
       AVG(prod_eolien)    AS eol_moy,
       AVG(prod_solaire)   AS sol_moy
FROM conso_horaire
GROUP BY saison;


-- Requête 6 : Top 5 jours de pointe
SELECT strftime('%Y-%m-%d', datetime) AS jour,
       MAX(conso_mw) AS conso_max
FROM conso_horaire
GROUP BY jour
ORDER BY conso_max DESC
LIMIT 5;
