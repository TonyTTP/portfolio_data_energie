

-- centrale | type    | production_mw | region
-------- | ------- | ------------- | ------
--A        | éolien  | 320           | Nord
--B        | solaire | 150           | Sud
--C        | éolien  | 415           | Nord
--D        | solaire | 200           | Sud
--E        | nucléaire| 2000         | Est
--F        | nucléaire| 1800         | Est

DROP TABLE IF EXISTS production_energie;
CREATE TABLE production_energie (
    centrale TEXT,
    type     TEXT,
    production_mw INT,
    region   TEXT
);

INSERT INTO production_energie VALUES
('A','éolien', 320, 'Nord'),
('B','solaire', 150, 'Sud'),
('C','éolien', 415, 'Nord'),
('D','solaire', 200, 'Sud'),
('E','nucléaire', 2000, 'Est'),
('F','nucléaire', 1800, 'Est');




SELECT type,SUM(production_mw) FROM production_energie
GROUP BY type
ORDER BY SUM(production_mw) DESC;



SELECT count(centrale),region,AVG(production_mw) FROM production_energie
GROUP BY region
HAVING AVG(production_mw) > 500
ORDER BY AVG(production_mw) DESC;
