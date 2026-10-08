import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app_env


def test_app_environment():
    assert app_env in ["development", "production"]
