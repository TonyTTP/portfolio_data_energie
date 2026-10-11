import pandas as pd
from datetime import datetime, timedelta
from fetch_entsoe import (COUNTRY_CODES,format_entsoe_date,request_entsoe,)

def get_day_ahead_prices(country_code, start_date,end_date):

    end_exclusive = (datetime.strptime(end_date, "%Y-%m-%d")+
                     timedelta(days=1)).strftime("%Y%m%d") + "0000"

    params = {
        "documentType": "A44",
        "in_Domain": country_code,
        "out_Domain": country_code,
        "periodStart": format_entsoe_date(start_date),
        "periodEnd": end_exclusive,
    }

    root = request_entsoe(params)

    if root is None:
        return None
    records = []
    for series in root.findall(".//{*}TimeSeries"):

        for period in series.findall(".//{*}Period"):

            start_element = period.find("./{*}timeInterval/{*}start")
            resolution_element = period.find("./{*}resolution")

            if (start_element is None or resolution_element is None
                or start_element.text is None or resolution_element.text is None):
                continue

            start = pd.to_datetime(start_element.text, utc=True)
            resolution = resolution_element.text

            if resolution == "PT15M":
                step = 15
            elif resolution == "PT30M":
                step = 30
            elif resolution == "PT60M":
                step = 60
            else:
                print(f"Résolution non gérée : {resolution}")
                continue

            for point in period.findall("./{*}Point"):

                position = point.find("./{*}position")
                price = point.find("./{*}price.amount")

                if (position is None or price is None
                    or position.text is None or price.text is None):
                    continue
                try:
                    timestamp = start + pd.Timedelta(minutes=step * (int(position.text) - 1))

                    records.append({"datetime": timestamp,"price_eur_mwh": float(price.text),})

                except (ValueError, TypeError):
                    continue

    df = pd.DataFrame(records)
    if df.empty:
        print("Aucun prix disponible.")
        return None
    print(f"Prix spot : {len(df)} lignes")

    return df

if __name__ == "__main__":

    df = get_day_ahead_prices(
        COUNTRY_CODES["France"],
        "2024-10-01",
        "2024-10-07")

    if df is not None:
        print(df.head())
        print(df["price_eur_mwh"].describe())
