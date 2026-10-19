import os
import pytest
import allure
from playwright.sync_api import Page, Browser, BrowserContext
from pages.home_page import HomePage
from pages.book_details_page import BookDetailsPage
from pages.quotes_page import QuotesPage

os.environ.pop("NODE_OPTIONS", None)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "ignore_https_errors": True,
    }

@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)

@pytest.fixture
def details_page(page: Page) -> BookDetailsPage:
    return BookDetailsPage(page)

@pytest.fixture
def quotes_page(page: Page) -> QuotesPage:
    return QuotesPage(page)

@pytest.fixture
def mobile_page(playwright, browser: Browser) -> Page:
    iphone_13 = playwright.devices["iPhone 13 Pro"]
    context: BrowserContext = browser.new_context(
        **iphone_13,
        ignore_https_errors=True
    )
    page: Page = context.new_page()
    yield page
    context.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("mobile_page")
        if page:
            screenshot_bytes = page.screenshot(full_page=True)
            allure.attach(
                screenshot_bytes,
                name=f"Failure_Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )