from playwright.sync_api import Page
from utils.config import Urls
from utils.env import load_env


class BMSLoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_input = page.locator("#id_username")
        self.password_input = page.locator("#id_password")
        self.login_button = page.get_by_role("button", name="login", exact=True)

    def goto(self):
        self.page.goto(Urls.BMS_URL, wait_until="networkidle")

    def login(self, username: str, password: str):
        env = load_env()
        self.goto()
        self.username_input.fill(env["POS_USERNAME"])
        self.password_input.fill(env["POS_PASSWORD"])
        self.login_button.click()
