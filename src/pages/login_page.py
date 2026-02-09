from playwright.sync_api import Page, expect
from utils.config import Urls
from utils.env import load_env


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="Your Username")
        self.password_input = page.get_by_role("textbox", name="Enter password")
        self.login_button = page.get_by_role("button", name="Log in")
        self.payment_button = page.locator(".checkout-action")

    def goto_pos(self):
        self.page.goto(Urls.POS, wait_until="networkidle")

    def login(self):
        env = load_env()
        self.goto_pos()
        self.username_input.fill(env["POS_USERNAME"])
        self.password_input.fill(env["POS_PASSWORD"])
        self.login_button.click()
        expect(self.payment_button).to_be_visible(timeout=10_000)
