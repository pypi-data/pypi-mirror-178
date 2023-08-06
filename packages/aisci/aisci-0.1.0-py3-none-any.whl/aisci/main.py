import toml
from dotenv import load_dotenv

from aisci.secret import print_secret

APP_CONFIG = toml.load("pyproject.toml")["app"]

load_dotenv()


def app():
    """This is the main entrypoint to your application"""
    print(f"This is {APP_CONFIG['APP_NAME']}. Let's build some cool python apps!")
    print(f"{APP_CONFIG['APP_STR_HELLO']}")
    print_secret()


def test():
    """This is the entrypoint to your test suite"""
    print("Running tests...")
