# Projet 18 — Prévision de consommation électrique avec XGBoost et SHAP

Prévision de la consommation électrique française à partir de l'historique, de la météo et de variables temporelles, avec comparaison de modèles (Random Forest, XGBoost), interprétabilité SHAP et diagnostic des erreurs de prévision.

## Architecture

- `sql/` : création des tables `eco2mix` et `meteo`, vue `v_ml_features`, requêtes de validation
- `data/` : chargement, nettoyage, création des variables, entraînement, évaluation, analyse SHAP et diagnostic
- `app/` : application Streamlit (Dashboard, Prévisions, Anomalies)

## Lancer le projet

```bash
pip install -r requirements.txt
```

1. Créer `database/energy.db` avec `sql/01_create_tables.sql`, y importer les données eco2mix et météo, puis exécuter `sql/02_import_features.sql`.
2. Entraîner et évaluer les modèles :
   ```bash
   cd data
   python evaluate.py
   python shape_analysis.py
   python diagnose.py
   ```
3. Lancer l'application :
   ```bash
   streamlit run app/main.py
   ```
