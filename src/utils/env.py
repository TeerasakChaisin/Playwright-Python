import os
from dotenv import load_dotenv
from pathlib import Path

def load_env():
    env = os.getenv("ENV", "dev")
    root = Path(__file__).resolve().parents[2]
    env_file = root / f".env.{env}"

    if not env_file.exists():
        raise FileNotFoundError(f"{env_file} not found")

    load_dotenv(env_file)