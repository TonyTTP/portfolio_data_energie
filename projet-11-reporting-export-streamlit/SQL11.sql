--Requete 1 : Delta semaine et semaine précédente
SELECT region,ROUND(AVG(CASE WHEN date >= date('now','7 days') THEN conso_mw END),0) AS conso_semaine,
ROUND(AVG(CASE WHEN date >= date('now','14 days') AND date <= date('7 days','14 days') THEN conso_mw END),0) AS conso_semaine_prece
FROM conso_journaliere
GROUP BY region;