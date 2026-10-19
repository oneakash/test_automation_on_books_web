from playwright.sync_api import Page, Locator, expect
import allure


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    @allure.step("Navigate back to previous page")
    def go_back(self) -> None:
        self.page.go_back(wait_until="domcontentloaded")

    def verify_url(self, expected_url: str) -> None:
        expect(self.page).to_have_url(expected_url)

    def verify_title(self, expected_title: str) -> None:
        expect(self.page).to_have_title(expected_title)