import sqlite3
import pandas as pd 

DATABASE = "database.db"

def connection(DATABASE):
    return sqlite3.connect(DATABASE)

def store_rte(DATABASE):
    connect = connexion()
    df.to_sql("eco2mix",connect, if_exists="replace", index=False)
    connect.close()
    print(f"nombre de lignes RTE : {len(df)}")

def store_meteo(DATABASE):
    connect = connexion()
    df.to_sql("meteo",connect, if_exists="replace", index=False)
    connect.close()
    print(f"nombre de lignes meteo : {len(df)}")

def read_table(table_name):

    conn = create_connection()
    df = pd.read_sql(f"SELECT * FROM {table_name}",conn)
    conn.close()
    return df

if __name__ == "__main__":
    print(f"Connexion SQLite configurée : "f"{DATABASE}")


