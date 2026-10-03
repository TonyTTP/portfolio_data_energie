-- VUE 1 : DONNÉES NATIONALES

DROP VIEW IF EXISTS v_national;
CREATE VIEW v_national AS SELECT ROW_NUMBER() OVER (ORDER BY date_heure) AS id,
date_heure,
DATE(date_heure) AS date,
CAST(strftime('%Y',date_heure) AS INTEGER) AS année,
CAST(strftime('%m',date_heure) AS INTEGER) AS mois,
CAST(strftime('%d',date_heure) AS INTEGER) AS jour,
CAST(strftime('%H',date_heure) AS INTEGER) AS heure,
CAST(strftime('%M',date_heure) AS INTEGER) AS minute,
consommation,
eolien,
solaire,
hydraulique,
renouvelable,
ROUND("part_renouvel_%",1) AS part_renouvelable_pct
FROM eco2mix_natio;


-- VUE 2 : DIMENSION DATE

DROP VIEW IF EXISTS v_dim_date;
CREATE VIEW v_dim_date AS
SELECT DISTINCT
DATE(date_heure) AS date,
CAST(strftime('%Y',date_heure) AS INTEGER) AS annee,
CAST(strftime('%m',date_heure) AS INTEGER) AS mois,
CAST(strftime('%d',date_heure) AS INTEGER) AS jour,
CASE CAST(strftime('%m',date_heure) AS INTEGER)
WHEN 1 THEN 'Janvier'
WHEN 2 THEN 'Février'
WHEN 3 THEN 'Mars'
WHEN 4 THEN 'Avril'
WHEN 5 THEN 'Mai'
WHEN 6 THEN 'Juin'
WHEN 7 THEN 'Juillet'
WHEN 8 THEN 'Aout'
WHEN 9 THEN 'Septembre'
WHEN 10 THEN 'Octobre'
WHEN 11 THEN 'Novembre'
WHEN 12 THEN 'Decembre'
END AS nom_mois,
CASE
WHEN CAST(strftime('%m',date_heure) AS INTEGER) IN (12,1,2) THEN 'Hiver'
WHEN CAST(strftime('%m',date_heure) AS INTEGER) IN (3,4,5) THEN 'Printemps'
WHEN CAST(strftime('%m',date_heure) AS INTEGER) IN (6,7,8) THEN 'Ete'
ELSE 'Automne'
END AS nom_saison,
CASE
WHEN CAST(strftime('%w',date_heure) AS INTEGER) IN (0,6) THEN 'Weekend'
ELSE 'Jour de semaine'
END AS type_jour
FROM eco2mix_natio
ORDER BY date;

-- VUE 3 : DONNÉES RÉGIONALES

DROP VIEW IF EXISTS v_regional;
CREATE VIEW v_regional AS
SELECT ROW_NUMBER() OVER (ORDER BY date_heure, libelle_region) AS fact_id,
    date_heure,
    DATE(date_heure) AS date,
    libelle_region AS region,
    CAST(strftime('%Y',date_heure) AS INTEGER) AS Année,
    CAST(strftime('%m',date_heure) AS INTEGER) AS Mois,
    CAST(strftime('%d',date_heure) AS INTEGER) AS Jour,
    CAST(strftime('%H',date_heure) AS INTEGER) AS Heure,
    CAST(strftime('%M',date_heure) AS INTEGER) AS Minute,  
    consommation,
    eolien,
    solaire,
    hydraulique,
    renouvelable,
    ROUND("part_renouvel_%",1) AS part_renouvelable_pct
FROM eco2mix_region;

-- VUE 4 : KPIs NATIONAUX
DROP VIEW IF EXISTS kpi_calcul;
CREATE VIEW kpi_calcul AS
SELECT ROUND(AVG(consommation),2) AS conso_moy,
ROUND(MAX(consommation),2) AS conso_max,
ROUND(MIN(consommation),2) AS conso_min,
ROUND(AVG(renouvelable),2) AS prod_renouv_moy,
ROUND(AVG("part_renouvel_%"),2) AS part_moy_renouv
FROM eco2mix_natio;

-- VUE 5 : KPIs PAR RÉGION
DROP VIEW IF EXISTS kpi_reg;
CREATE VIEW kpi_reg AS 
SELECT libelle_region AS region,
ROUND(AVG(consommation),2) AS conso_moy,
ROUND(MAX(consommation),2) AS conso_max,
ROUND(MIN(consommation),2) AS conso_min,
ROUND(AVG(renouvelable),2) AS prod_renouv_moy,
ROUND(AVG("part_renouvel_%"),2) AS part_moy_renouv
FROM eco2mix_region
GROUP BY libelle_region;

SELECT * FROM kpi_reg;



