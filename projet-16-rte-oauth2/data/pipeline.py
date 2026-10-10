from datetime import datetime, timedelta
from fetch_rte_oauth import RTEDataFetcher
from clean import clean_consumption, clean_generation, clean_exchanges
from store import get_connection, save_dataframe, create_views


def run_pipeline(days_back=30):
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    print(f"Période : du {start} au {end}")

    fetcher = RTEDataFetcher()
    df_conso = clean_consumption(fetcher.get_consumption(start, end))
    df_prod = clean_generation(fetcher.get_generation(start, end))
    df_echanges = clean_exchanges(fetcher.get_exchanges(start, end))

    conn = get_connection()
    try:
        save_dataframe(df_conso, "consommation", conn)
        save_dataframe(df_prod, "production", conn)
        save_dataframe(df_echanges, "echanges", conn)
        if df_echanges is not None and not df_echanges.empty:
            create_views(conn)  
    finally:
        conn.close()


if __name__ == "__main__":
    run_pipeline(days_back=30)
