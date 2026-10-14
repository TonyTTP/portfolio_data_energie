SELECT run_name,experiment, ROUND(rmse,2) as rmse, ROUND(r2,4) as r2,
datetime
FROM ml_runs
ORDER BY datetime DESC;

SELECT * FROM v_best_models
ORDER BY rmse ASC;

SELECT run_name,n_estimators,learning_rate,max_depth,ROUND(rmse,2) as rmse, ROUND(r2,4) as r2
FROM ml_runs 
WHERE rmse NOT NULL
ORDER BY rmse DESC;

SELECT experiment, COUNT(*) AS nombre_runs, ROUND(AVG(rmse),2) as rmse_moyen, ROUND(MIN(rmse),2) AS meilleur_rmse
FROM ml_runs
GROUP BY experiment;

SELECT run_name,datetime, ROUND(rmse,2) AS rmse,
ROUND(rmse - LAG(rmse) OVER (ORDER BY datetime),2) AS ecart_name
FROM ml_runs
WHERE rmse IS NOT NULL
ORDER BY datetime DESC;