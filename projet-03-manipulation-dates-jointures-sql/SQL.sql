-- T'as ces 2 tables :

-- Table "conso" :
-- date       | region | conso_mw
-- 2023-01-01 | Paris  | 850
-- 2023-01-02 | Paris  | 920
-- 2023-01-03 | Paris  | 780
-- 2023-01-01 | Lyon   | 420
-- 2023-01-02 | Lyon   | 380
-- 2023-01-03 | Lyon   | 450

-- Table "objectifs" :
-- region | objectif_mw
-- Paris  | 900
-- Lyon   | 400

DROP TABLE IF EXISTS conso;
CREATE TABLE conso (
	date1 TEXT,
	region TEXT,
	conso_mw INT
	); 
	
INSERT INTO conso VALUES 
('2023-01-01','Paris',850),
('2023-01-02','Paris',920),
('2023-01-03','Paris',780),
('2023-01-01','Lyon',420),
('2023-01-02','Lyon',380),
('2023-01-03','Lyon',450);

DROP TABLE IF EXISTS objectif ;
CREATE TABLE objectif (
	region TEXT,
	objectif_mw INT
	);
	
INSERT INTO objectif VALUES 
('Paris',900),
('Lyon',400);


SELECT c.region,c.date1,c.conso_mw, o.objectif_mw, c.conso_mw - o.objectif_mw AS ecart
FROM conso c 
INNER JOIN objectif o
ON c.region = o.region
WHERE c.conso_mw > o.objectif_mw;



DROP TABLE IF EXISTS conso_journaliere;
CREATE TABLE conso_journaliere (
	date1 TEXT,
	region TEXT,
	conso_mw INT
	); 
	
INSERT INTO conso_journaliere VALUES 
('2023-01-01','Paris',850),
('2023-01-02','Paris',920),
('2023-01-03','Paris',780),
('2023-01-01','Lyon',420),
('2023-01-02','Lyon',380),
('2023-01-03','Lyon',450);

SELECT *FROM (
SELECT date1,region,conso_mw, LAG(conso_mw) OVER ( PARTITION BY region ORDER BY date1) AS conso_preced,
conso_mw - LAG(conso_mw) OVER ( PARTITION BY region ORDER BY date1) AS variations
FROM conso_journaliere
)
WHERE (variations > 50); 






