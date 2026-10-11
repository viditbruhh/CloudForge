import os
import subprocess
import sys
from pathlib import Path

APP_FILE = Path(__file__).resolve().parents[1] / "src" / "app.py"


def run_app(environment=None):
    env = os.environ.copy()
    env.pop("APP_ENV", None)

    if environment is not None:
        env["APP_ENV"] = environment

    result = subprocess.run(
        [sys.executable, str(APP_FILE)],
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def test_default_environment():
    assert run_app() == (
        "CloudForge application is running in development environment!"
    )


def test_production_environment():
    assert run_app("production") == (
        "CloudForge application is running in production environment!"
    )


def test_custom_environment():
    assert run_app("testing") == (
        "CloudForge application is running in testing environment!"
    )
