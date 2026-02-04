from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "src" / "data"
IMPORT_DIR = DATA_DIR / "import"
ORDER_FILE = DATA_DIR / "importlist_data.yaml"


def load_import_sequence():
    with open(ORDER_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    result = []

    for import_type in data.get("import_types", []):
        file_path = IMPORT_DIR / f"{import_type}.xlsx"

        if file_path.exists():
            result.append((import_type, str(file_path)))

    return result
