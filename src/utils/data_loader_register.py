from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

def load_yaml(filename):
    file_path = DATA_DIR / filename
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
