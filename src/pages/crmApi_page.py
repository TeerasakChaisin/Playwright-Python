from playwright.sync_api import Page


class crmAPI:
    def __init__(self, page: Page):
        self.page = page

        self.imports = page.get_by_role("link", name="Imports")
        self.addImport = page.get_by_role("link", name="เพิ่ม import")
        self.importList = page.get_by_label("Importer:")
        self.importFile = page.locator('input[type="file"]')
        self.saveandEdit = page.get_by_role("button", name="บันทึกและกลับมาแก้ไข")
        self.runImport = page.get_by_role("link", name="Run import")

    def select_import_type(self, import_type: str):
        self.importList.select_option(label=import_type)
        self.saveandEdit.click()
        self.runImport.click()
