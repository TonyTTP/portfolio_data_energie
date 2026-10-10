import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).parent.parent / "database" / "energy_oauth.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def save_dataframe(df, table_name, conn):
    if df is None or df.empty:
        print(f"Aucune ligne à enregistrer dans {table_name}")
        return


    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"{len(df)} lignes enregistrées dans {table_name}")


def create_views(conn):

    conn.executescript("""
        DROP VIEW IF EXISTS v_balance_france;

        CREATE VIEW v_balance_france AS
        SELECT
            datetime,
            SUM(CASE WHEN receiver = 'FRANCE' THEN flow_mw ELSE 0 END) AS imports_mw,
            SUM(CASE WHEN sender   = 'FRANCE' THEN flow_mw ELSE 0 END) AS exports_mw,
            SUM(CASE WHEN sender   = 'FRANCE' THEN  flow_mw
                     WHEN receiver = 'FRANCE' THEN -flow_mw
                     ELSE 0 END)                                  AS net_export_mw
        FROM echanges
        GROUP BY datetime
        ORDER BY datetime;
    """)
    conn.commit()
    print("Vue v_balance_france créée")
