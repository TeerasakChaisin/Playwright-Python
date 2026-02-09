import os
from dotenv import load_dotenv
from pathlib import Path


def load_env():
    env_name = os.getenv("ENV", "dev")
    env_file = Path(f".env.{env_name}")

    if not env_file.exists():
        raise FileNotFoundError(f"{env_file} not found")

    load_dotenv(env_file, override=True)
    return dict(os.environ)
