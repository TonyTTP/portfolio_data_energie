# Projet 19 — MLOps : suivi d'expériences avec MLflow

Prévision de la consommation électrique française avec XGBoost, à partir des données eco2mix temps réel de RTE (API ODRE), avec suivi des expériences, comparaison des réglages et registre de modèles dans MLflow.

## Architecture

- `data/` : récupération eco2mix (`fetch_rte.py`), nettoyage et variables (`clean.py`), stockage SQLite (`store.py`)
- `models/` : entraînement (`train.py`), évaluation (`evaluate.py`), prédiction (`predict.py`)
- `mlflow_tracking/` : expériences (`experiments.py`), comparaison (`compare.py`), registre du meilleur modèle (`registry.py`)
- `sql/` : table `ml_runs`, vue `v_best_models` et requêtes d'analyse
- `app/` : application Streamlit (Dashboard, Prévisions, Suivi MLOps)

## Lancer le projet

Depuis la racine du projet :

```bash
pip install -r requirements.txt
python data/store.py
python models/train.py
python models/evaluate.py
python mlflow_tracking/experiments.py
python mlflow_tracking/compare.py
python mlflow_tracking/registry.py
streamlit run app/main.py
```

Interface MLflow : `mlflow ui --backend-store-uri sqlite:///mlflow.db`
