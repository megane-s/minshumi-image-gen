import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str):
    return os.environ[key]


def get_env_with_default(key: str, default: str):
    return os.environ.get(key, default)
