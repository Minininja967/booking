# tests/conftest.py
import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="function")
def page():
    """Запускаем браузер перед каждым тестом и закрываем после"""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()