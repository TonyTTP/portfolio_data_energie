import pandas as pd
import numpy as np

# Données avec valeurs manquantes
df = pd.DataFrame({
    "date"    : pd.date_range("2023-01-01", periods=10),
    "region"  : ["Paris"]*5 + ["Lyon"]*5,
    "conso_mw": [420, np.nan, 450, np.nan, 390,
                 280, 310, np.nan, 295, 320],
    "temp_c"  : [2, 3, np.nan, 1, 4,
                 8, np.nan, 7, 9, 6]
})



print("le nombre de valeur nulle",df.isnull().sum())



df["conso_mw"] = df["conso_mw"].fillna(df["conso_mw"].mean())



df["temp_c"] = df["temp_c"].ffill()
print(df)





moyenne = df["conso_mw"].mean().round(2)
ecartype = df["conso_mw"].std().round(2)
maximum = df["conso_mw"].max()
minimum = df["conso_mw"].min()


resultat = df.groupby("region")["conso_mw"].agg(["mean","max","min","std"])
print(resultat)




df["Z_score"] = (df["conso_mw"] - moyenne) / ecartype

print(df)

dates = pd.date_range(start="01-01-2023",periods=180,freq="D")

df1 = pd.DataFrame({
    "date" : dates,
    "conso_mw" : np.random.randint(200,800,size=180),
    "temp" : np.random.randint(-5,30,size=180),
    "region" : np.tile(["Paris","Lyon"],90)
})


conso_moy = df.resample("M",on="date")["conso_mw"].mean()
print("la conso moy est", conso_moy)

top3 = df1.nlargest(3, "conso_mw")
print("le top 3 est",top3)



correlation = df1[["conso_mw","temp"]].corr()
print("la correlation est",correlation)




# Projet : Détection anomalies consommation

import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

dates = pd.date_range("2023-01-01", periods=365, freq="D")
np.random.seed(42)

conso_base = 500 + 200 * np.sin(
    np.linspace(0, 2*np.pi, 365)
)


bruit = np.random.normal(0, 30, 365)


anomalies = np.zeros(365)
idx_anomalies = np.random.choice(365, 10, replace=False)
anomalies[idx_anomalies] = np.random.randint(-400, 400, 10)

df = pd.DataFrame({
    "date"    : dates,
    "conso_mw": conso_base + bruit + anomalies
})



moyenne = df["conso_mw"].mean()
ecart_type = df["conso_mw"].std()

seuil_haut = moyenne + 2 * ecart_type
seuil_bas = moyenne - 2 * ecart_type

df["anomalie"] = (
    (df["conso_mw"] > seuil_haut) | (df["conso_mw"] < seuil_bas))

print(df[df["anomalie"]== True])


conn = sqlite3.connect("conso_annuelle.db")

df.to_sql("conso_annuelle",conn,if_exists="replace",index=False)


requete = """
SELECT
    strftime('%m', date) AS mois,
    COUNT(*) AS nb_anomalies
FROM conso_annuelle
WHERE anomalie = 1
GROUP BY mois
ORDER BY nb_anomalies DESC LIMIT 1
"""

resultat = pd.read_sql_query(requete, conn)

print(resultat)

conn.close()




plt.figure(figsize=(12,6))

plt.plot( df["date"], df["conso_mw"],color="blue",label="Consommation")

plt.scatter(df.loc[df["anomalie"], "date"], df.loc[df["anomalie"], "conso_mw"], color="red", label="anomalie")

plt.title("Détection d'anomalies de consommation")
plt.xlabel("Date")
plt.ylabel("Consommation (MW)")
plt.legend()
plt.grid()

plt.show()