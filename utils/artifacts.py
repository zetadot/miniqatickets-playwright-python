from __future__ import annotations

import allure
from playwright.sync_api import Page


def attach_page_screenshot(page: Page, name: str) -> None:
    screenshot = page.screenshot(full_page=True)
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )
