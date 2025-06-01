# tests/conftest.py
import os
import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="function")
def page():
    """Запускаем браузер перед каждым тестом и закрываем после"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:3000")
