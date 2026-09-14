--récupérons le classement des temperature les plus élevé à la moins élevé

SELECT ville,
ROUND(AVG(temperature_2m),1) AS temperature_moyenne,
ROUND(MAX(temperature_2m),1) AS temperature_max,
ROUND(MIN(temperature_2m),1) AS temperature_min,
ROUND(AVG(precipitation),1) AS pluie_moyenne,
ROUND(AVG(windspped_10m),1) AS vitesse_moyenne
COUNT(*) AS nbre_mesures
FROM meteo_horaire
WHERE time < datetime('now')
GROUP BY ville
ORDER BY temperature_moyenne DESC;

--Classement top10 des plus froides
SELECT ville, 
DATE(time) AS jour,
ROUND(AVG(temperature_2m),1) AS temperature_moyenne_jour,
ROUND(MIN(temperature_2m),1) AS temperature_min_jour
FROM meteo_horaire
WHERE time < datetime('now')
GROUP BY ville,jour
ORDER BY temperature_moyenne_jour ASC LIMIT 10;

--Analysons les 7 prochains jours de prévisions.

SELECT ville, DATE(time) AS jour,
ROUND(AVG(temperature_2m),1) AS temperature_moy_prevue,
ROUND(SUM(precipitation),1) AS precipitation_cumulée_prevue,
ROUND(MAX(windspeed_10m),1) AS vitesse_du_vent_max_prevue
FROM meteo_horaire
WHERE time >= datetime('now')
Group BY ville,jour
ORDER BY ville,jour




