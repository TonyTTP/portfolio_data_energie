
import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range("2023-01-01", periods=8760, freq="h")


day_of_year = dates.dayofyear

df_rte = pd.DataFrame({
    "datetime"      : dates,
    "conso_mw"      : 45000 + 15000 * np.cos(2 * np.pi * day_of_year / 365)
                      + np.random.normal(0, 2000, len(dates)),
    "prod_nucleaire" : 35000 + 5000 * np.cos(2 * np.pi * day_of_year / 365)
                      + np.random.normal(0, 1500, len(dates)),
    "prod_eolien"   : 5000 + 2000 * np.cos(2 * np.pi * day_of_year / 365)
                      + np.random.normal(0, 800, len(dates)),
    "prod_solaire"  : np.maximum(0, 3000 * np.sin(2 * np.pi * (day_of_year - 80) / 365)
                      + np.random.normal(0, 300, len(dates))),
    "region"        : np.tile(
                      ["Paris", "Lyon", "Marseille", "Lille", "Bordeaux"],
                      len(dates) // 5 + 1)[:len(dates)]
})

print("=== INFO ===")
print(df_rte.info())

print("\n=== DESCRIBE ===")
print(df_rte.describe())


print("\n=== DONNÉES PAR RÉGION ===")

print(df_rte.groupby("region").size())


print("autre manière :", df_rte["region"].value_counts())

df_rte["heure"] = df_rte["datetime"].dt.hour

conso_moyenne_heure = df_rte.groupby("heure")["conso_mw"].mean()

print("\n=== CONSO MOYENNE PAR HEURE ===")
print(conso_moyenne_heure)


heure_max = conso_moyenne_heure.idxmax()
conso_max = conso_moyenne_heure.max()

print(f"\nHeure avec la plus forte consommation moyenne : {heure_max}h")
print(f"Consommation moyenne : {conso_max:.2f} MW")




df_rte["heure"] = df_rte["datetime"].dt.hour
df_rte["jour"] = df_rte["datetime"].dt.dayofweek
df_rte["mois"] = df_rte["datetime"].dt.month

def saison(mois):
    if mois in [12, 1, 2]:
        return "hiver"
    elif mois in [3, 4, 5]:
        return "printemps"
    elif mois in [6, 7, 8]:
        return "été"
    else:
        return "automne"

df_rte["saison"] = df_rte["mois"].apply(saison)

# 2. Consommation moyenne par saison
conso_saison = df_rte.groupby("saison")["conso_mw"].mean()
print(conso_saison)

# 3. Semaine vs week-end
df_rte["type_jour"] = np.where(df_rte["jour"] < 5,
                               "semaine",
                               "week-end")

conso_type = df_rte.groupby("type_jour")["conso_mw"].mean()
print(conso_type)

# Avec df_rte :

import pandas as pd
import matplotlib.pyplot as plt



total_nucleaire = df_rte["prod_nucleaire"].sum()
total_eolien = df_rte["prod_eolien"].sum()
total_solaire = df_rte["prod_solaire"].sum()

total_prod = total_nucleaire + total_eolien + total_solaire

mix = pd.Series({
    "Nucléaire": 100 * total_nucleaire / total_prod,
    "Éolien": 100 * total_eolien / total_prod,
    "Solaire": 100 * total_solaire / total_prod
})

print("Mix énergétique annuel (%)")
print(mix)



df_rte["mois"] = df_rte["datetime"].dt.month

mix_mensuel = pd.DataFrame(
    df_rte.groupby("mois")
    [["prod_nucleaire","prod_eolien","prod_solaire"]].mean()
)


print(mix_mensuel)




mix_mensuel.plot(
    kind="bar",
    stacked=True,
    figsize=(10,6)
)

plt.title("Mix énergétique moyen par mois")
plt.xlabel("Mois")
plt.ylabel("Production moyenne (MW)")
plt.legend()
plt.show()




mois_max_solaire = mix_mensuel["prod_solaire"].idxmax()
mois_max_eolien = mix_mensuel["prod_eolien"].idxmax()

print("Mois max solaire :", mois_max_solaire)
print("Mois max éolien :", mois_max_eolien)



df_rte["z_score"] = (
    (df_rte["conso_mw"] - df_rte["conso_mw"].mean())
    / df_rte["conso_mw"].std()
)

# Pics (anomalies)
df_rte["pic"] = df_rte["z_score"] > 2


print(df_rte.groupby("saison")["pic"].sum())

print(df_rte[df_rte["pic"]].groupby("heure").size().idxmax())



import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt


import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt



df_rte["prod_solaire"] = df_rte["prod_solaire"].clip(lower=0)

df_rte["heure"] = df_rte["datetime"].dt.hour
df_rte["mois"] = df_rte["datetime"].dt.month

def saison(m):
    if m in [12,1,2]:
        return "Hiver"
    elif m in [3,4,5]:
        return "Printemps"
    elif m in [6,7,8]:
        return "Été"
    else:
        return "Automne"

df_rte["saison"] = df_rte["mois"].apply(saison)



courbe_charge = (df_rte.groupby("heure")["conso_mw"].mean())

# B) Mix énergétique par saison

mix_saison = (df_rte.groupby("saison")
[["prod_nucleaire","prod_eolien","prod_solaire"]].mean())

top5 = (df_rte.nlargest(5, "conso_mw")[["datetime","conso_mw"]])

print(top5)

# D) Corrélations

corr = (df_rte[["prod_nucleaire","prod_eolien","prod_solaire"]].corr())

print(corr)



df_rte["z_score"] = ((df_rte["conso_mw"] -df_rte["conso_mw"].mean())
/ df_rte["conso_mw"].std())

pics_conso = df_rte[df_rte["z_score"] > 2]


mix_mensuel = (df_rte.groupby("mois")
    [["prod_nucleaire","prod_eolien","prod_solaire"]].mean())



conn = sqlite3.connect("rte_dashboard.db")
df_rte.to_sql( "conso_horaire",conn,if_exists="replace",index=False)

mix_mensuel.to_sql("mix_mensuel",conn,if_exists="replace")

pics_conso.to_sql("pics_conso",conn,if_exists="replace",index=False)
conn = sqlite3.connect("rte_dashboard.db")

df_rte.to_sql("conso_horaire", conn, if_exists="replace", index=False)
mix_mensuel.to_sql("mix_mensuel", conn, if_exists="replace")
pics_conso.to_sql("pics_conso", conn, if_exists="replace", index=False)

conn.close()


fig, axes = plt.subplots(2,2,figsize=(15,10))

# Courbe de charge

axes[0,0].plot(courbe_charge)
axes[0,0].set_title("Courbe de charge moyenne")

# Camembert énergétique

parts = [
    df_rte["prod_nucleaire"].sum(),
    df_rte["prod_eolien"].sum(),
    df_rte["prod_solaire"].sum()
]

axes[0,1].pie(
    parts,
    labels=["Nucléaire","Éolien","Solaire"],
    autopct="%1.1f%%"
)
axes[0,1].set_title("Mix énergétique")

# Consommation par saison

df_rte.groupby("saison")["conso_mw"].mean().plot(kind="bar",ax=axes[1,0])

axes[1,0].set_title("Conso moyenne par saison")

# Scatter

axes[1,1].scatter(df_rte["prod_nucleaire"],df_rte["conso_mw"], alpha=0.4)

axes[1,1].set_title("Conso vs Nucléaire")

plt.tight_layout()
plt.show()

# ==========================
# ETAPE 5 : Rapport
# ==========================

conso_moy = df_rte["conso_mw"].mean()
conso_max = df_rte["conso_mw"].max()

mois_max = (
    df_rte.groupby("mois")["conso_mw"]
    .mean()
    .idxmax()
)

part_nuc = (
    100 *
    df_rte["prod_nucleaire"].sum()
    /
    (
        df_rte["prod_nucleaire"].sum()
        + df_rte["prod_eolien"].sum()
        + df_rte["prod_solaire"].sum()
    )
)

nb_anomalies = len(pics_conso)

print(f"""
  RAPPORT CONSOMMATION ÉLECTRIQUE 2023 

Conso moyenne annuelle : {conso_moy:.0f} MW
Pic maximum            : {conso_max:.0f} MW
Mois le plus consommateur : {mois_max}
Part nucléaire         : {part_nuc:.1f} %
Nombre d'anomalies     : {nb_anomalies}

""")