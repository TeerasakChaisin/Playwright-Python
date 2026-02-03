import os
from utils.env import load_env

load_env()

POS_USERNAME = os.getenv("POS_USERNAME")
POS_PASSWORD = os.getenv("POS_PASSWORD")

_REQUIRED = {
    "POS_USERNAME": POS_USERNAME,
    "POS_PASSWORD": POS_PASSWORD,
}

missing = [k for k, v in _REQUIRED.items() if not v]
if missing:
    raise ValueError(f"Missing env vars: {', '.join(missing)}")
