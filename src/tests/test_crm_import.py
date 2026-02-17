from utils.data_import_file_loader import load_import_sequence

def test_import_files(crm_api):
    for import_type, file_path in load_import_sequence("importlist_data.yaml"):
        crm_api.open_import_page()
        crm_api.select_import_type(import_type)
        crm_api.upload_file(file_path)
        crm_api.save()
        crm_api.run()
