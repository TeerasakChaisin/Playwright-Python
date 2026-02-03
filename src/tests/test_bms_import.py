from pathlib import Path
from utils.data_bms_import_file_loader import get_all_bms_import_files


def test_import_all_bms_excel_files(bms_page):
    bms_page.open_master_data()

    for file_path in get_all_bms_import_files():
        downloads = bms_page.upload_file(str(file_path))
        input_stem = Path(file_path).stem

        for download in downloads:
            suggested = download.suggested_filename.lower()

            if "success" in suggested:
                status = "Success"
            elif "failed" in suggested:
                status = "Failed"
            else:
                status = "Unknown"

            download.save_as(f"downloads/{input_stem}_{status}.xlsx")
