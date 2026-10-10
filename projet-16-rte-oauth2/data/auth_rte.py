import requests
from datetime import datetime, timedelta
import os
import base64
from dotenv import load_dotenv

load_dotenv()


class RTEAuthManager:
    TOKEN_URL = "https://digital.iservices.rte-france.com/token/oauth/"  # adresse du guichet

    def __init__(self):
        self.client_id = os.getenv("RTE_CLIENT_ID")
        self.client_secret = os.getenv("RTE_CLIENT_SECRET")

        self.token = None
        self.token_expiry = None

        if not self.client_id or not self.client_secret:
            raise ValueError("RTE_CLIENT_ID ou RTE_CLIENT_SECRET ne sont pas présents dans .env")

    def _encode_credentials(self):
        credentials = f"{self.client_id}:{self.client_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def get_token(self):
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token

        response = requests.post(
            self.TOKEN_URL,
            headers={"Authorization": f"Basic {self._encode_credentials()}"},
            timeout=10,
        )

        if response.status_code != 200:
            raise Exception(f"{response.status_code} : {response.text}")

        data = response.json()
        self.token = data["access_token"]
        expires_in = data.get("expires_in", 3600)
        self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 60)

        print(f"Token RTE valide jusqu'à {self.token_expiry:%H:%M:%S}")

        return self.token

    def get_headers(self):
        return {"Authorization": f"Bearer {self.get_token()}"}


if __name__ == "__main__":
    auth = RTEAuthManager()
    token = auth.get_token()
    print(f"Token : {token[:20]}...")
