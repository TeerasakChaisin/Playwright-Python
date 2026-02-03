import os
import requests
from utils.env import load_env

load_env()


class customer_wallet_detail:
    def __init__(self):
        self.base_url = os.getenv("API_CRM")
        if not self.base_url:
            raise ValueError("Missing API_CRM")

    def get_member(self, member_id: str, wallet_code: str):
        url = f"{self.base_url}/s2s/v1/member/{member_id}/"
        resp = requests.get(
            url,
            params={"wallet_code": wallet_code},
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()
