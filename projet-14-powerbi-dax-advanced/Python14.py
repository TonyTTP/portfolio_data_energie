import datetime from datetime
import requests
import pandas as pd


nb_jour = 30

url_national = (
    "https://data.rte-france.com"
    "/api/explore/v2.1/catalog/datasets"
    "/eco2mix-national-cons-def/records"
)

url_regional = (
    "https://data.rte-france.com"
    "/api/explore/v2.1/catalog/datasets"
    "/eco2mix-regional-tr/records"
)

def recup(url,where,size=10000):
    tout_enr = []
    offset = 0
    while True :
        params = {
            "timezone" : "Europe/Paris",
            "offset" : offset,
            "where" : where,
            "limit" : size,
            "order_by" : "daye_heure ASC"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get("results", [])

        if not records:
            break
        tout_enr.extend(records)
        if len(records) < size:
            break 
        offset += records

    return pd.DataFrame(tout_enr)

