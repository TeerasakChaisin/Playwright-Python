from utils.env import load_env

load_env()

pytest_plugins = [
    "fixtures.auth",
]
