import os
import yaml
from pathlib import Path
from utils.env import load_env

load_env()

_DATA = None


def _load_yaml():
    global _DATA
    if _DATA is None:
        path = Path(__file__).resolve().parents[1] / "data" / "pos_data.yaml"
        with open(path, "r", encoding="utf-8") as f:
            _DATA = yaml.safe_load(f)
    return _DATA


def get_customers():
    return _load_yaml()["customers"]


def get_products():
    return _load_yaml()["products"]


def get_tiers():
    return _load_yaml()["tiers"]


POS_USERNAME = os.getenv("POS_USERNAME")
POS_PASSWORD = os.getenv("POS_PASSWORD")

_REQUIRED = {
    "POS_USERNAME": POS_USERNAME,
    "POS_PASSWORD": POS_PASSWORD,
}

missing = [k for k, v in _REQUIRED.items() if not v]
if missing:
    raise ValueError(f"Missing env vars: {', '.join(missing)}")
