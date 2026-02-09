from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "src" / "data"

def load_yaml(filename: str):
    file_path = DATA_DIR / filename
    with open(file_path, encoding="utf-8") as f:
        return yaml.safe_load(f)
