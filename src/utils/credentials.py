import os
from utils.env import load_env

load_env()


class Credentials:
    POS_USER = os.getenv("POS_USER")
    POS_PASSWORD = os.getenv("POS_PASSWORD")

    CRM_API_USER = os.getenv("CRM_API_USER")
    CRM_API_PASSWORD = os.getenv("CRM_API_PASSWORD")

    @staticmethod
    def validate_pos():
        missing = []
        if not Credentials.POS_USER:
            missing.append("POS_USER")
        if not Credentials.POS_PASSWORD:
            missing.append("POS_PASSWORD")
        if missing:
            raise ValueError(f"Missing credential env vars: {', '.join(missing)}")
