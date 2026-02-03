from playwright.sync_api import Page, expect
from utils.config import Urls


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.get_by_role("textbox", name="Your Username")
        self.password_input = page.get_by_role("textbox", name="Enter password")
        self.login_button = page.get_by_role("button", name="Log in")
        self.payment_button = page.locator(".checkout-action")

    def goto_pos(self):
        self.page.goto(Urls.POS, wait_until="networkidle")

    def login_pos(self, username: str, password: str):
        self.goto_pos()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_login_successful(self):
        expect(self.payment_button).to_be_visible(timeout=10_000)
