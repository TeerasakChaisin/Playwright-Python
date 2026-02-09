from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.crmapiLogin_page import crmapiPage
from pages.crmApi_page import crmAPI
from utils.yaml_loader import load_yaml
from utils.data_import_file_loader import build_import_files


def test_register_then_import(context):
    config = load_yaml("register2import_data.yaml")

    page = context.new_page()

    LoginPage(page).login()
    RegisterPage(page).register(config["new_user"])

    crmapiPage(page).login()
    crm = crmAPI(page)

    for import_type, file_path in build_import_files("register2import_data.yaml"):
        crm.import_file(import_type, file_path)
