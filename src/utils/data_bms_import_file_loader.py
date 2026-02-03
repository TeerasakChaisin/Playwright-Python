from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
BMS_IMPORT_DIR = BASE_DIR / "src" / "data" / "bms_import"


def get_all_bms_import_files():
    return sorted(BMS_IMPORT_DIR.glob("*.xlsx"))
