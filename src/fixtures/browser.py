# src/fixtures/browser.py
import pytest
from playwright.sync_api import sync_playwright, Page
from utils.config import Urls
from pages.login_page import LoginPage
from utils.credentials import Credentials

@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture(scope="session")
def page(browser_context):
    page = browser_context.new_page()
    yield page
    page.close()

@pytest.fixture(scope="session", autouse=True)
def login(page: Page):
    login_page = LoginPage(page)
    login_page.login_pos(Credentials.POS_USER, Credentials.POS_PASSWORD)
    login_page.expect_login_successful()
