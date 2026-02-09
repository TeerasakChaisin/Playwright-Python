import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.crmapiLogin_page import crmapiPage
from pages.crmApi_page import crmAPI
from pages.bmsLogin_page import BMSLoginPage
from pages.bms_page import BMSPage

from utils.data_loader_pos import POS_USERNAME, POS_PASSWORD


def _ensure_credentials():
    if not POS_USERNAME or not POS_PASSWORD:
        pytest.fail("Credentials missing")


@pytest.fixture
def pos_page(page: Page) -> Page:
    LoginPage(page).login()
    return page

@pytest.fixture
def crm_api(page: Page) -> crmAPI:
    crm_login = crmapiPage(page)
    crm_login.login()
    return crmAPI(page)

@pytest.fixture
def bms_page(page: Page) -> BMSPage:
    login_page = BMSLoginPage(page)
    login_page.login(POS_USERNAME, POS_PASSWORD)

    return BMSPage(page)
