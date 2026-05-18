from __future__ import annotations

import os
from collections.abc import Generator
from pathlib import Path

import allure
import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Browser, BrowserContext, Page, Playwright, sync_playwright

from utils.artifacts import attach_page_screenshot

load_dotenv()


def _as_bool(value: str | None, default: bool = True) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:3000").rstrip("/")


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    browser = playwright_instance.chromium.launch(headless=_as_bool(os.getenv("HEADLESS"), default=True))
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser, base_url: str) -> Generator[BrowserContext, None, None]:
    context = browser.new_context(base_url=base_url, viewport={"width": 1440, "height": 900})
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    return context.new_page()


@pytest.fixture()
def api_request(playwright_instance: Playwright, base_url: str) -> Generator[APIRequestContext, None, None]:
    request_context = playwright_instance.request.new_context(base_url=base_url)
    yield request_context
    request_context.dispose()


@pytest.fixture(autouse=True)
def attach_final_screenshot(page: Page, request: pytest.FixtureRequest) -> Generator[None, None, None]:
    yield
    if page.is_closed():
        return
    attach_page_screenshot(page, f"final-state-{request.node.name}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")
    if page is None or page.is_closed():
        return

    attach_page_screenshot(page, f"failure-{item.name}")
