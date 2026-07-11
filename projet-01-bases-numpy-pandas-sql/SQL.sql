-Contexte : une table energie avec ces colonnes :
--date |        region | consommation_mw | type_energie
--2024-01-01    Paris      450              solaire
--2024-01-01    Lyon       230              éolien
--2024-01-02    Paris      480              solaire
--2024-01-02    Marseille  310              hydraulique
DROP TABLE IF EXISTS table_energie;

CREATE TABLE table_energie (
    datedujour DATE,
    region     TEXT,
    consommation_mw INT,
    type_energie TEXT,
    PRIMARY KEY (datedujour, region, type_energie)
    );
   
INSERT INTO table_energie VALUES

('2024-01-01','Paris',450,'solaire'),
('2024-01-01','Lyon',230,'éolien'),
('2024-01-02','Paris',480,'solaire'),
('2024-01-02','Marseille',310, 'hydraulique');



SELECT * FROM table_energie
WHERE region = 'Paris'
ORDER BY consommation_mw DESC LIMIT 1;





SELECT region, AVG(consommation_mw) AS moy_conso
FROM table_energie
GROUP BY region
HAVING AVG(consommation_mw) > 200;
ORDER BY consommation_mw ASC LIMIT 4;