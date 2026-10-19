from playwright.sync_api import Page, Locator, expect
import allure


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        """Navigates to the specified URL and waits for DOM content to load."""
        self.page.goto(url, wait_until="domcontentloaded")

    def get_current_url(self) -> str:
        """Returns the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.page.title()

    @allure.step("Navigate back to previous page")
    def go_back(self) -> None:
        """Navigates back in browser history and waits for DOM load."""
        self.page.go_back(wait_until="domcontentloaded")

    def verify_url(self, expected_url: str) -> None:
        """Asserts that the current page URL matches the expected URL."""
        expect(self.page).to_have_url(expected_url)

    def verify_title(self, expected_title: str) -> None:
        """Asserts that the page title matches the expected title."""
        expect(self.page).to_have_title(expected_title)