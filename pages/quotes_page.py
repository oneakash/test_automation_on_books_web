from playwright.sync_api import Page, Locator, expect
import allure
from pages.base_page import BasePage
from utils.config import Config

class QuotesPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.header_title: Locator = page.locator("h1 a")
        self.login_link: Locator = page.locator("a[href='/login']")
        self.username_input: Locator = page.locator("input#username")
        self.password_input: Locator = page.locator("input#password")
        self.submit_button: Locator = page.locator("input[type='submit'][value='Login']")
        self.logout_link: Locator = page.locator("a[href='/logout']")

    @allure.step("Navigate to Quotes to Scrape Homepage")
    def open_homepage(self) -> None:
        self.navigate(Config.QUOTES_BASE_URL)
        expect(self.header_title).to_be_visible()
        expect(self.header_title).to_have_text("Quotes to Scrape")

    @allure.step("Navigate to Login page via Login link")
    def click_login_link(self) -> None:
        expect(self.login_link).to_be_visible()
        expect(self.login_link).to_be_enabled()
        self.login_link.click()

    @allure.step("Verify Login page loaded")
    def verify_login_page_loaded(self) -> None:
        expect(self.page).to_have_url(f"{Config.QUOTES_BASE_URL}login")
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.submit_button).to_be_visible()

    @allure.step("Perform login with username: {username}")
    def login(self, username: str, password: str) -> None:
        self.username_input.clear()
        self.username_input.press_sequentially(username, delay=50)
        expect(self.username_input).to_have_value(username)

        self.password_input.clear()
        self.password_input.press_sequentially(password, delay=50)
        expect(self.password_input).to_have_value(password)

        self.submit_button.click()
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Verify authenticated state and Logout link availability")
    def verify_logged_in_state(self) -> None:
        expect(self.logout_link).to_be_visible()
        expect(self.logout_link).to_be_enabled()