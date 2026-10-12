import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

APP_FILE = Path(__file__).resolve().parents[1] / "src" / "app.py"


def start_app(environment="development", port=8765):
    env = os.environ.copy()
    env["APP_ENV"] = environment
    env["PORT"] = str(port)

    process = subprocess.Popen(
        [sys.executable, str(APP_FILE)],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    url = f"http://127.0.0.1:{port}"

    for _ in range(50):
        if process.poll() is not None:
            raise RuntimeError("Application exited before becoming ready")

        try:
            urllib.request.urlopen(f"{url}/health", timeout=0.2)
            return process, url
        except (urllib.error.URLError, TimeoutError):
            time.sleep(0.1)

    process.terminate()
    raise RuntimeError("Application did not become ready")


def stop_app(process):
    process.terminate()
    try:
        process.wait(timeout=3)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()


def test_health_endpoint():
    process, url = start_app()

    try:
        with urllib.request.urlopen(f"{url}/health") as response:
            data = json.loads(response.read())

        assert response.status == 200
        assert data["status"] == "healthy"
        assert data["application"] == "CloudForge"
        assert data["environment"] == "development"
    finally:
        stop_app(process)


def test_root_endpoint():
    process, url = start_app()

    try:
        with urllib.request.urlopen(url) as response:
            body = response.read().decode()

        assert response.status == 200
        assert body == (
            "CloudForge application is running in development environment!"
        )
    finally:
        stop_app(process)


def test_unknown_endpoint_returns_404():
    process, url = start_app()

    try:
        try:
            urllib.request.urlopen(f"{url}/unknown")
            assert False, "Expected HTTP 404"
        except urllib.error.HTTPError as error:
            assert error.code == 404
            assert json.loads(error.read()) == {"error": "Not found"}
    finally:
        stop_app(process)


def test_production_environment():
    process, url = start_app(environment="production", port=8766)

    try:
        with urllib.request.urlopen(f"{url}/health") as response:
            data = json.loads(response.read())

        assert data["environment"] == "production"
    finally:
        stop_app(process)
