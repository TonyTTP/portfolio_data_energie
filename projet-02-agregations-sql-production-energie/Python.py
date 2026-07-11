#1
#Contexte : Tu travailles sur des données de consommation électrique.
#Crée un array Numpy avec ces consommations journalières (en MW) :
#120, 135, 98, 142, 110, 155, 130

import numpy as np
import pandas as pd

conso = np.array([120, 135, 98, 142, 110, 155, 130])
print(conso)
#Puis affiche :
#1. L'array complet
#2. La consommation du 3ème jour
#3. La consommation maximale
conso3 = conso[2]
print(conso3)
consomax = conso.max()
print(conso.max())

#Avec le même array :
#1. Calcule la moyenne de consommation
#2. Affiche tous les jours où la conso dépasse 130 MW
#3. Multiplie toutes les valeurs par 1000   (convertir MW en KW)

moy = conso.mean()
print("la moyenne est",moy)
std = conso.std()
print("l'écart type",std)
#2
#Crée un DataFrame pandas avec ces données :
#- 5 jours de la semaine (lundi → vendredi)
#- Consommation matin  : 120, 135, 98, 142, 110
#- Consommation soir   : 180, 190, 160, 200, 175

df1 = pd.DataFrame({
    "matin" : [120, 135, 98, 142, 110],
    "soir" : [180, 190, 160, 200, 175]
})

#Puis :
#1. Affiche les infos du DataFrame (.info())



#print(df.info())
#print(df.describe().round(0))


#2. Calcule la consommation totale par jour
 #  (matin + soir)

df1["totale"] = df1["matin"] + df1["soir"]

print(df1)
#3. Quel jour a la plus haute conso totale ?

print("la conso max est",df1["totale"].max())

#3
#Étape 1 (Python) :
#Crée ce DataFrame :
#  date       | region      | conso_mw
#  2023-01-01 | Paris       | 450
#  2023-01-01 | Lyon        | 230
#  2023-01-02 | Paris       | 480
#  2023-01-02 | Lyon        | 210
#  2023-01-03 | Paris       | 420
#  2023-01-03 | Lyon        | 250

df2 = pd.DataFrame({
    "date" : ["2023-01-01","2023-01-01","2023-01-02","2023-01-02","2023-01-03","2023-01-03"],
    "region" : ["Paris","Lyon","Paris","Lyon","Paris","Lyon"],
    "conso_mw" : ["450","230","480","210","420","250"]
})

#Étape 2 (Python) :
#Stocke ce DataFrame dans une base SQLite
#appelée "formation.db", table "energie"

import sqlite3

connect = sqlite3.connect("formation.db")
df2.to_sql("energie", connect, if_exists="replace")

#Étape 3 (SQL dans Jupyter) :
#Écris une requête qui calcule
#la consommation moyenne par région
#et affiche le résultat directement dans Jupyter

query = """
SELECT region,AVG(conso_mw) AS conso_moy
FROM energie
GROUP BY region;
"""

result=  pd.read_sql(query,connect)
print(result)

