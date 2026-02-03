from utils.data_import_file_loader import load_import_files


def test_import_files(crm_api):
    import_jobs = load_import_files()

    crm_api.goto_importer()

    for import_name, file_path in import_jobs:
        crm_api.select_import_type(import_name)
        crm_api.importFile.set_input_files(file_path)
        crm_api.saveandEdit.click()
