from playwright.sync_api import Page
from playwright.sync_api import TimeoutError


class BMSPage:
    def __init__(self, page: Page):
        self.page = page

        self.sideBar = page.locator(".toggle-sidebar-button")
        self.masterData = page.get_by_role("link", name="Master Data")
        self.customer = page.get_by_role("link", name="Customer / Supplier")
        self.customerName = page.get_by_role("link", name="Customer/Supplier Name")
        self.import_file_input = page.locator('input[type="file"]')
        self.save_button = page.get_by_role("button", name="SAVE")

    def open_master_data(self):
        self.sideBar.click()
        self.masterData.click()
        self.customer.click()
        self.customerName.click()

    def upload_file(self, file_path: str):
        self.page.reload()
        self.import_file_input.set_input_files(file_path)

        with self.page.expect_download(timeout=600000) as download_info:
            self.save_button.click(timeout=600000)

        return [download_info.value]
