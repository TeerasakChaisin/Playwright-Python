from pathlib import Path
import yaml
import time

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"


def load_yaml(filename):
    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    ts = int(time.time())

    user = data["new_user"]
    user["first_name"] = f'{user["first_name"]}-{ts}'
    user["phone_number"] = f'{user["phone_number"]}{str(ts)[-6:]}'
    user["email"] = f"test{ts}@gmail.com"

    return data
