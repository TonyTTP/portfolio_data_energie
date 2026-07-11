-- Table "conso_regions" :
-- date       | region | conso_mw | temp_c
-- 2023-01-01 | Paris  | 850      | 2
-- 2023-01-01 | Lyon   | 420      | 5
-- 2023-01-02 | Paris  | 920      | 0
-- 2023-01-02 | Lyon   | 380      | 6
-- 2023-01-03 | Paris  | 780      | 3
-- 2023-01-03 | Lyon   | 450      | 4

CREATE TABLE conso_regions (
    date TEXT,
    region TEXT,
    conso_mw REAL,
    temp_c REAL
);

INSERT INTO conso_regions VALUES
('2023-01-01','Paris',850,2),
('2023-01-01','Lyon',420,5),
('2023-01-02','Paris',920,0),
('2023-01-02','Lyon',380,6),
('2023-01-03','Paris',780,3),
('2023-01-03','Lyon',450,4);


SELECT *
FROM conso_regions
WHERE region = 'Paris'
  AND conso_mw > (
      SELECT AVG(conso_mw)
      FROM conso_regions
  );
