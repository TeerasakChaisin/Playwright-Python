import os
from utils.env import load_env

load_env()


class Urls:
    POS = os.getenv("POS_URL")
    CRM_API = os.getenv("CRM_API_URL")
    REGISTER = os.getenv("REGISTER_URL")
    BMS_URL = os.getenv("BMS_URL")
    CRM_API_IMPORT_URL = os.getenv("CRM_API_IMPORT_URL")


_REQUIRED_URLS = {
    "POS_URL": Urls.POS,
    "CRM_API_URL": Urls.CRM_API,
    "CRM_API_IMPORT_URL": Urls.CRM_API_IMPORT_URL,
    "REGISTER_URL": Urls.REGISTER,
}

missing = [name for name, value in _REQUIRED_URLS.items() if not value]
if missing:
    raise ValueError(f"Missing env vars: {', '.join(missing)}")
