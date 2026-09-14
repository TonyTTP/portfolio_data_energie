--récupérons le classement des temperature les plus élevé à la moins élevé

SELECT ville,
ROUND(AVG(temperature_2m),1) AS temperature_moyenne,
ROUND(MAX(temperature_2m),1) AS temperature_max,
ROUND(MIN(temperature_2m),1) AS temperature_min,
ROUND(AVG(precipitation),1) AS pluie_moyenne,
ROUND(AVG(windspeed_10m),1) AS vitesse_moyenne,
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
AND time < datetime('now', '+7 days')
GROUP BY ville,jour
ORDER BY ville,jour

--Heures les plus venteuses

SELECT ville,CAST(strftime('%H', time) AS INTEGER) AS heure,
ROUND(MAX(windspeed_10m),1) AS vitesse_max
FROM meteo_horaire
WHERE time < datetime('now')
GROUP BY ville, heure
ORDER BY vitesse_max DESC
LIMIT 3;


--Couverture nuageuse et température


SELECT CAST(strftime('%H', time) AS INTEGER) AS heure,
ROUND(AVG(temperature_2m),1) AS temperature_moyenne,
CASE 
WHEN cloud_cover < 0.25 THEN 'Ensoleillé'
WHEN cloud_cover >= 0.25 AND cloud_cover < 0.50 THEN 'Peu nuageux'
WHEN cloud_cover >= 0.50 AND cloud_cover < 0.75 THEN 'Nuageux'
ELSE 'Très nuageux'
END AS couverture,
COUNT(*) AS nbreheures
FROM meteo_horaire
GROUP BY ville, heure, couverture
ORDER BY ville, temperature_moyenne DESC
LIMIT 10;


