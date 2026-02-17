from pathlib import Path
from utils.yaml_loader import load_yaml
from utils.excel_builder import build_tier_update_excel, build_wallet_excel

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "src" / "data"
IMPORT_DIR = DATA_DIR / "import"
RESULT_FILE = BASE_DIR / "created_users.txt"

def load_member_ids():
    with open(RESULT_FILE, encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]

def build_import_files(yaml_name: str):
    config = load_yaml(yaml_name)
    member_ids = load_member_ids()

    result = []

    for import_type, cfg in config["import_types"].items():
        file_path = IMPORT_DIR / f"{import_type}.xlsx"

        if cfg["type"] == "tier":
            build_tier_update_excel(member_ids, cfg, file_path)

        elif cfg["type"] == "wallet":
            build_wallet_excel(member_ids, cfg["columns"], file_path)

        result.append((import_type, str(file_path)))

    return result

def load_import_sequence(yaml_name: str):
    data = load_yaml(yaml_name)

    result = []
    for import_type in data["import_types"]:
        file_path = IMPORT_DIR / f"{import_type}.xlsx"
        result.append((import_type, str(file_path)))

    return result
