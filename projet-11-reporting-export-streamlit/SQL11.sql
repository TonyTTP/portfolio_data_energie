--Requete 1 : Delta semaine et semaine précédente
SELECT region,ROUND(AVG(CASE WHEN date >= date('now','-7 days') THEN conso_mw END),0) AS conso_semaine,
ROUND(AVG(CASE WHEN date >= date('now','-14 days') AND date <= date('now','-7 days') THEN conso_mw END),0) AS conso_semaine_prece
FROM conso_journaliere
GROUP BY region;

--Requete 2 : Heure de pointe par saison

SELECT CASE WHEN CAST(strftime('%m', date) AS INTEGRER) IN (12,1,2) THEN 'hiver'

SELECT CASE WHEN CAST(strftime('%m',date) AS INTEGRER) IN (3,4,5) THEN 'printemps'

SELECT CASE WHEN CAST(strftime('%m',date) AS INTEGRER) IN (6,7,8) THEN 'été'

ELSE 'automne' END AS saison

CAST(strftime('%H', date) AS INTEGER)AS heure, ROUND(AVG(conso_mw), 0) AS conso_moy
FROM conso_journaliere 

GROUP BY region,heure

ORDER BY region, heure;

Requete 3 : variation % du meme jour année différente

WITH consommation AS(SELECT date,conso_mw,region,
LAG(conso_mw,365) OVER(PARTITION BY region ORDER BY date) AS conso_preced
 FROM conso_journaliere )


SELECT date, region, conso_mw, conso_preced,
ROUND(((conso_mw - conso_preced)/conso_preced)*100,2) AS variation_pourcentage

FROM consommation
WHERE conso_preced IS NOT NULL
ORDER BY date;



