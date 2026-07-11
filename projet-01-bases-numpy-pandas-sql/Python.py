

import numpy as np
import pandas as pd

conso = np.array([120, 135, 98, 142, 110, 155, 130])
print(conso)

conso3 = conso[2]
print(conso3)
consomax = conso.max()
print(conso.max())



moy = conso.mean()
print("la moyenne est",moy)
std = conso.std()
print("l'écart type",std)


df1 = pd.DataFrame({
    "matin" : [120, 135, 98, 142, 110],
    "soir" : [180, 190, 160, 200, 175]
})




df1["totale"] = df1["matin"] + df1["soir"]

print(df1)


print("la conso max est",df1["totale"].max())

#3
#Étape 1 (Python) :

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
    "conso_mw" : [450,230,480,210,420,250]
})



import sqlite3

connect = sqlite3.connect("formation.db")
df2.to_sql("energie", connect, if_exists="replace")


query = """
SELECT region,AVG(conso_mw) AS conso_moy
FROM energie
GROUP BY region;
"""

result=  pd.read_sql(query,connect)
print(result)