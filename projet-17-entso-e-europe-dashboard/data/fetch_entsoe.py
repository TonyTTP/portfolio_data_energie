#les imports
#charger .env
#recup la clé de l'API
#base url
#code pays
#lit le texte "2026-10-11" et le transforme en vraie date Python
#strftime réécrit cette date sans tirets, "20261011", puis on ajoute "0000"

import pandas as pd
import os
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

load_dotenv()

API_KEY = os.getenv("ENTSOE_API_KEY")
BASE_URL = "https://web-api.tp.entsoe.eu/api"


COUNTRY_CODES = {
    "France": "10YFR-RTE------C",
    "Allemagne": "10Y1001A1001A82H",
    "Espagne": "10YES-REE------0",
    "Italie": "10Y1001A1001A73I",
    "Belgique": "10YBE----------2",
    "Pays-Bas": "10YNL----------L",
    "Portugal": "10YPT-REN------W",
    "Pologne": "10YPL-AREA-----S",
    "Norvège": "10YNO-1--------2",
}

def format_entsoe_date(date_str):
    date = datetime.strptime(date_str,"%Y-%m-%d")
    return date.strftime("%Y%m%d") + "0000"

def request_entsoe(params):
    if not API_KEY :
        raise ValueError("ENTSOE_API_KEY absent du fichier .env")
    params["securityToken"] = API_KEY
    try:
        response = requests.get(BASE_URL,params=params,timeout=15)
        response.raise_for_status()
        return ET.fromstring(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Erreur API ENTSO-E : {e}")
        return None
    except ET.ParseError as e:
        print(f"Erreur de lecture XML : {e}")
        return None

def parse_time_series(root,value_tag="quantity"):
    records = []
    for series in root.findall(".//{*}TimeSeries"):
        for period in series.findall(".//{*}Period"):

            start_element = period.find("./{*}timeInterval/{*}start")
            resolution_element = period.find("./{*}resolution")

            if (start_element is None or
                resolution_element is None or
                start_element.text is None or
                resolution_element.text is None):
                continue

            start = pd.to_datetime(start_element.text, utc=True)

            resolution = resolution_element.text

            if resolution.startswith("PT"):
                if resolution.endswith("M"):
                    step = int(resolution[2:-1])
                elif resolution.endswith("H"):
                    step = int(resolution[2:-1]) * 60
                else:
                    continue
            else:
                continue

            for point in period.findall("./{*}Point"):
                position = point.find("./{*}position")
                value = point.find(f"./{{*}}{value_tag}")

                if (
                    position is None
                    or value is None
                    or position.text is None
                    or value.text is None
                ):
                    continue

                try:
                    # Les positions XML commencent à 1
                    timestamp = start + pd.Timedelta(
                        minutes=step * (
                            int(position.text) - 1
                        )
                    )

                    records.append({
                        "datetime": timestamp,
                        "value": float(value.text)
                    })

                except (ValueError, TypeError):
                    continue

    return pd.DataFrame(records)


class ENTSOEDataFetcher:
    def get_consumption(self, country_code, start_date, end_date):
        end_exclusive = (
            datetime.strptime(end_date, "%Y-%m-%d")
            + timedelta(days=1)).strftime("%Y%m%d") + "0000"

        params = {
            "documentType": "A65",
            "processType": "A16",
            "outBiddingZone_Domain": country_code,
            "periodStart": format_entsoe_date(start_date),
            "periodEnd": end_exclusive,
        }

        root = request_entsoe(params)

        if root is None:
            return None

        df = parse_time_series(root, "quantity")

        if df.empty:
            print("Aucune donnée de consommation.")
            return None

        df = df.rename(columns={"value": "conso_mw"})

        print(f"Consommation : {len(df)} lignes")

        return df

if __name__ == "__main__":

    fetcher = ENTSOEDataFetcher()

    df = fetcher.get_consumption(
        COUNTRY_CODES["France"],
        "2024-10-01",
        "2024-10-07"
    )

    if df is not None:
        print(df.head())
        print(df.info())
