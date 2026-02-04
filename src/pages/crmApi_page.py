from playwright.sync_api import Page
from utils.config import Urls


class crmAPI:
    def __init__(self, page: Page):
        self.page = page

        self.importList = page.get_by_label("Importer:")
        self.importFile = page.locator('input[type="file"]')
        self.saveandEdit = page.get_by_role("button", name="บันทึกและกลับมาแก้ไข")
        self.runImport = page.get_by_role("link", name="Run import")

    def open_import_page(self):
        self.page.goto(f"{Urls.CRM_API_IMPORT_URL}", wait_until="networkidle")
        self.page.wait_for_load_state("networkidle")

    def select_import_type(self, import_type: str):
        self.importList.select_option(label=import_type)

    def upload_file(self, file_path: str):
        self.importFile.set_input_files(file_path)

    def save(self):
        self.saveandEdit.click()
        self.page.wait_for_load_state("networkidle")

    def run(self):
        self.runImport.click()
        self.page.wait_for_load_state("networkidle")
        self.open_import_page()
