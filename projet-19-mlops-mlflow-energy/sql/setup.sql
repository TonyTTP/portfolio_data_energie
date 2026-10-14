DROP TABLE IF EXISTS ml_runs;
CREATE TABLE IF NOT EXISTS ml_runs(
 id INTEGER PRIMARY KEY,
run_id TEXT NOT NULL UNIQUE,
 run_name TEXT NOT NULL,
experiment TEXT NOT NULL,
datetime TEXT DEFAULT(datetime('now')),
n_estimators INTEGER,
learning_rate REAL,
max_depth INTEGER,
rmse REAL,
r2 REAL,
mape REAL,
n_samples INTEGER, n_features INTEGER,
model_status TEXT DEFAULT 'evaluate');

DROP VIEW IF EXISTS v_best_models;
CREATE VIEW IF NOT EXISTS v_best_models AS
    SELECT 
    experiment,run_id,run_name,
    ROUND(rmse,2) AS rmse,
    ROUND(r2,4) AS r2,
    n_estimators,
    learning_rate,
    max_depth,
    datetime

    FROM ml_runs 
    WHERE rmse IS NOT NULL
    AND rmse=(SELECT MIN(sub.rmse)
    FROM ml_runs AS sub
    WHERE sub.experiment = ml_runs.experiment);

