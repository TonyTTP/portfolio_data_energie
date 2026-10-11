import os
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from dotenv import load_dotenv

#charger .env()
#recupérer API_KEY
#Base url
#country code

#fonction entsoe

#fonction requests
#si pas API  Value Error
#params, response = , response.raise ET.fromstring

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

PSR_TYPES = {
    "B01": "Biomasse",
    "B02": "Lignite",
    "B04": "Gaz",
    "B05": "Charbon",
    "B06": "Fioul",
    "B09": "Géothermie",
    "B10": "Hydraulique STEP",
    "B11": "Hydraulique fil de l'eau",
    "B12": "Hydraulique lacs",
    "B14": "Nucléaire",
    "B15": "Autres renouvelables",
    "B16": "Solaire",
    "B17": "Déchets",
    "B18": "Éolien en mer",
    "B19": "Éolien terrestre",
    "B20": "Autres",
}


def format_entsoe_date(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%Y%m%d") + "0000"

def request_entsoe(params):
    if not API_KEY:
        raise ValueError("ENTSOE_API_KEY absent du fichier .env")
    params["securityToken"] = API_KEY
    reponse = requests.get(BASE_URL,params=params,timeout=15)
    reponse.raise_for_status()
    return ET.fromstring(reponse.content)

def parse_time_series(root,value_tag="quantity"):
    records = []
    for series in root.findall(".//{*}TimeSeries"):
        psr_element = series.find("./{*}MktPSRType/{*}psrType")
        psr_type = psr_element.text if psr_element is not None else None

        for period in series.findall(".//{*}Period"):

            start_element = period.find("./{*}timeInterval/{*}start")
            resolution_element = period.find("./{*}resolution")
            if (
                start_element is None or
                resolution_element is None or
                start_element.text is None or
                resolution_element.text is None ) :
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

                if (position is None or
                    value is None or
                    position.text is None or
                    value.text is None):
                    continue

                try:
                    timestamp = start + pd.Timedelta(
                        minutes=step * (
                            int(position.text) - 1
                        )
                    )

                    records.append({
                        "datetime": timestamp,
                        "value": float(value.text),
                        "psr_type": psr_type,
                    })

                except (ValueError, TypeError):
                    continue

    return pd.DataFrame(records)

class ENTSOEDataFetcher:
    def get_consumption(self, country_code, start_date, end_date):

        end_exclusive = (
            datetime.strptime(end_date, "%Y-%m-%d")
            + timedelta(days=1)
        ).strftime("%Y%m%d") + "0000"

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

        df = df.drop(columns="psr_type").rename(columns={"value": "conso_mw"})

        print(f"Consommation : {len(df)} lignes")

        return df

    def get_generation(self, country_code, start_date, end_date):

        end_exclusive = (
            datetime.strptime(end_date, "%Y-%m-%d")
            + timedelta(days=1)
        ).strftime("%Y%m%d") + "0000"

        params = {
            "documentType": "A75",
            "processType": "A16",
            "in_Domain": country_code,
            "periodStart": format_entsoe_date(start_date),
            "periodEnd": end_exclusive,
        }

        root = request_entsoe(params)

        if root is None:
            return None

        df = parse_time_series(root, "quantity")

        if df.empty:
            print("Aucune donnée de production.")
            return None

        df["production_type"] = df["psr_type"].map(PSR_TYPES).fillna(df["psr_type"])
        df = df.rename(columns={"value": "production_mw"})

        print(f"Production : {len(df)} lignes, {df['production_type'].nunique()} filières")

        return df

if __name__ == "__main__":

    fetcher = ENTSOEDataFetcher()

    df = fetcher.get_generation(
        COUNTRY_CODES["France"],
        "2024-10-01",
        "2024-10-07"
    )

    if df is not None:
        print(df.head())
        print(df.info())
