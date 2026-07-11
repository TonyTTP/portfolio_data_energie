-- Table "conso_journaliere" :
-- date | conso_mw | temperature


SELECT date,conso_mw,
AVG(conso_mw) OVER ( ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW ) AS moyenne_mobile_7j
FROM conso_journaliere
ORDER BY date




SELECT date,conso_mw, LAG(conso_mw, 7) OVER (ORDER BY date) AS conso_semaine_prec, ROUND((conso_mw - LAG(conso_mw, 7) OVER (ORDER BY date))
/ LAG(conso_mw, 7) OVER (ORDER BY date) * 100, 2 ) AS variation_pct
FROM conso_journaliere
WHERE ABS((conso_mw - LAG(conso_mw, 7) OVER (ORDER BY date))/ LAG(conso_mw, 7) OVER (ORDER BY date) * 100) > 10

ORDER BY date;
