from playwright.sync_api import Page
from utils.config import Urls


class BMSLoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator("#id_username")
        self.password_input = page.locator("#id_password")
        self.login_button = page.get_by_role("button", name="login", exact=True)

    def goto(self):
        self.page.goto(Urls.BMS_URL, wait_until="networkidle")

    def login(self, username: str, password: str):
        self.goto()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
