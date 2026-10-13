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

1. Importer 2 ans de données eco2mix (ODRE) et météo de Paris (Open-Meteo) dans `database/energy.db` :
   ```bash
   cd data
   python import_data.py
   ```
2. Entraîner et évaluer les modèles :
   ```bash
   python evaluate.py
   python shape_analysis.py
   python diagnose.py
   ```
3. Lancer l'application :
   ```bash
   streamlit run app/main.py
   ```
