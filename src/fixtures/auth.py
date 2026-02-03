import os
import pytest
from pages.login_page import LoginPage
from pages.crmapiLogin_page import crmapiPage
from pages.crmApi_page import crmAPI
from pages.bmsLogin_page import BMSLoginPage
from pages.bms_page import BMSPage

from utils.data_loader_pos import POS_USERNAME, POS_PASSWORD


@pytest.fixture
def login(page):
    if not POS_USERNAME or not POS_PASSWORD:
        pytest.fail("Credentials missing")

    login_page = LoginPage(page)
    login_page.login_pos(POS_USERNAME, POS_PASSWORD)
    login_page.expect_login_successful()


@pytest.fixture
def crm_api(page):
    if not POS_USERNAME or not POS_PASSWORD:
        pytest.fail("Credentials missing")

    login_page = crmapiPage(page)
    login_page.login(POS_USERNAME, POS_PASSWORD)

    return crmAPI(page)


@pytest.fixture
def bms_page(page):
    if not POS_USERNAME or not POS_PASSWORD:
        pytest.fail("Credentials missing")

    login_page = BMSLoginPage(page)
    login_page.login(POS_USERNAME, POS_PASSWORD)

    return BMSPage(page)
