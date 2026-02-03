from pathlib import Path
import yaml


def load_import_files():
    base_dir = Path(__file__).resolve().parents[1]
    yaml_path = base_dir / "data" / "importlist_data.yaml"

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    import_dir = base_dir / "data" / "import"

    result = []

    for import_type in data["import_types"]:
        file_path = import_dir / f"{import_type}.xlsx"
        if file_path.exists():
            result.append((import_type, str(file_path)))

    return result
