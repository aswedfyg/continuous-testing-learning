import os
import socket
import subprocess
import sys
import time
from collections.abc import Iterator
from pathlib import Path

import pytest
import requests
from playwright.sync_api import Page, sync_playwright


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", 0))
        return int(server_socket.getsockname()[1])


@pytest.fixture(scope="session")
def base_url() -> Iterator[str]:
    configured_url = os.getenv("BASE_URL")
    if configured_url:
        yield configured_url
        return
    
    port = _find_free_port()
    url = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                response = requests.get(f"{url}/health", timeout=1)
                if response.status_code == 200:
                    break
            except requests.RequestException:
                time.sleep(0.2)
        else:
            raise RuntimeError("Local test app did not start within 15 seconds")

        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


# @pytest.fixture
# def page() -> Iterator[Page]:
#     with sync_playwright() as playwright:
#         browser = playwright.chromium.launch()
#         page = browser.new_page()

#         try:
#             yield page
#         finally:
#             browser.close()

@pytest.fixture
def page(request: pytest.FixtureRequest) -> Iterator[Page]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()

        try:
            yield page
        finally:
            test_failed = request.node.rep_call.failed

            if test_failed:
                screenshot_dir = Path("reports/screenshots")
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                screenshot_path = screenshot_dir / f"{request.node.name}.png"
                page.screenshot(path=str(screenshot_path), full_page=True)

                trace_dir = Path("reports/traces")
                trace_dir.mkdir(parents=True, exist_ok=True)
                trace_path = trace_dir / f"{request.node.name}.zip"
                context.tracing.stop(path=str(trace_path))
            else:
                context.tracing.stop()

            browser.close()




@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[object]):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
