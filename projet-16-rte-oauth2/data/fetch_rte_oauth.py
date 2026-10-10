import requests
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from auth_rte import RTEAuthManager

PARIS = ZoneInfo("Europe/Paris")


def format_rte_date(date_str, add_days=0):
    # "2026-10-01" -> "2026-10-01T00:00:00+02:00" (le +01:00 / +02:00 s'adapte à l'heure d'hiver / d'été)
    date = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=add_days)
    return date.replace(tzinfo=PARIS).isoformat()


class RTEDataFetcher:
    BASE_URL = "https://digital.iservices.rte-france.com/open_api"

    def __init__(self):
        self.auth = RTEAuthManager()

    def _get(self, endpoint, params=None):
        url = f"{self.BASE_URL}/{endpoint}"
        for attempt in range(3):
            try:
                response = requests.get(url, headers=self.auth.get_headers(), params=params, timeout=15)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    self.auth.token = None  # token refusé : on en redemande un au prochain essai
                else:
                    print(f"Erreur {response.status_code} sur {endpoint} : {response.text}")
                    return None
            except requests.exceptions.RequestException as e:
                print(f"Erreur réseau (essai {attempt + 1}/3) : {e}")
        return None

    def _date_params(self, start_date, end_date):
        # end_date = minuit le lendemain pour inclure toute la dernière journée
        return {
            "start_date": format_rte_date(start_date),
            "end_date": format_rte_date(end_date, add_days=1),
        }

    def get_consumption(self, start_date, end_date):
        data = self._get("consumption/v1/short_term", params=self._date_params(start_date, end_date))
        if not data:
            return None

        records = []

        for item in data.get("short_term", []):
            for val in item.get("values", []):
                records.append({
                    "datetime": val["start_date"],
                    "conso_mw": val["value"],
                    "type": item["type"],
                })

        if not records:
            return None

        df = pd.DataFrame(records)
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        print(f"Consommation : {len(df)} lignes")
        return df

    def get_generation(self, start_date, end_date, production_type=None):
        params = self._date_params(start_date, end_date)

        if production_type:
            params["production_type"] = production_type

        data = self._get("actual_generation/v1/actual_generations_per_production_type", params=params)

        if not data:
            return None

        records = []

        for prod in data.get("actual_generations_per_production_type", []):
            prod_type = prod["production_type"]

            for val in prod.get("values", []):
                records.append({
                    "datetime": val["start_date"],
                    "production_mw": val["value"],
                    "production_type": prod_type,
                })

        if not records:
            return None

        df = pd.DataFrame(records)
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        print(f"Production : {len(df)} lignes")
        return df

    def get_exchanges(self, start_date, end_date):
        data = self._get("physical_flow/v1/physical_flows", params=self._date_params(start_date, end_date))

        if not data:
            return None

        records = []

        for flow in data.get("physical_flows", []):
            for val in flow.get("values", []):
                records.append({
                    "datetime": val["start_date"],
                    "flow_mw": val["value"],
                    "sender": flow["sender_country_name"],
                    "receiver": flow["receiver_country_name"],
                })

        if not records:
            return None

        df = pd.DataFrame(records)
        df["datetime"] = pd.to_datetime(df["datetime"], utc=True)
        print(f"Échanges : {len(df)} lignes")
        return df
