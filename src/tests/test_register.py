from pages.register_page import RegisterPage
from utils.data_loader_register import load_yaml

register_data = load_yaml("register_data.yaml")


def test_register_success(page):
    register = RegisterPage(page)
    register.register(register_data["new_user"])
