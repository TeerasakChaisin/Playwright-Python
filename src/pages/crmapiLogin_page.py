from playwright.sync_api import Page
from utils.config import Urls


class crmapiPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.get_by_role("textbox", name="Username:")
        self.password_input = page.get_by_role("textbox", name="รหัสผ่าน:")
        self.login_button = page.get_by_role("button", name="เข้าสู่ระบบ")

    def goto(self):
        self.page.goto(Urls.CRM_API, wait_until="networkidle")

    def login(self, username: str, password: str):
        self.goto()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
