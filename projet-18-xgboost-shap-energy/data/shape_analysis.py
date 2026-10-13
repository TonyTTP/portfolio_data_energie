from pathlib import Path 
import matplotlib.pyplot as plt 
import pandas as pd 
import shap
from train import train_models 

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def explain_model(result):
    pipeline = result["model"]
    X_test = result["X_test"]
    model = pipeline.named_steps["model"]
    imputer = pipeline.named_steps["imputer"]
    X_imputed = pd.DataFrame(imputer.transform(X_test),columns=X_test.columns,index=X_test.index)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_imputed)

    shap.plots.bar(shap_values,max_display=15,show=False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "shap_importance.png",dpi=150,bbox_inches="tight")
    plt.close()

    shap.plots.beeswarm(shap_values,max_display=15,show=False)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "shap_beeswarm.png",dpi=150,bbox_inches="tight")
    plt.close()

    if len(X_imputed) > 0:
        shap.plots.waterfall(shap_values[0],max_display=12,show=False)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "shap_waterfall.png",dpi=150,bbox_inches="tight")
        plt.close()

    print("Graphiques SHAP enregistrés dans", OUTPUT_DIR)

if __name__ == "__main__":
    results = train_models()
    explain_model(results["xgboost"])
