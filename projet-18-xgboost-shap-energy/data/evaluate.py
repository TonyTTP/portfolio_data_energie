from pathlib import Path
 
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from train import train_models 

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs" 
OUTPUT_DIR.mkdir(exist_ok=True)

def evaluate_models(results):
    rows = []
    for name, result in results.items():
        y_true = result["y_test"]
        y_pred = result["predictions"]
        rows.append({"modele" : name, "MAE_MW" : mean_absolute_error(y_true,y_pred), "RMSE_MW" : mean_squared_error(y_true,y_pred)**0.5,
                     "R2" : r2_score(y_true,y_pred)})
    comparison = pd.DataFrame(rows)
    comparison = comparison.sort_values("RMSE_MW")
    comparison.to_csv(OUTPUT_DIR/"model_comparison.csv", index=False)
    print(comparison.to_string(index=False))
    return comparison 


if __name__ == "__main__":
    results = train_models()
    evaluate_models(results)
