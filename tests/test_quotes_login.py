import pytest
import allure
from pages.quotes_page import QuotesPage
from utils.config import Config

@allure.epic("Quotes to Scrape UI Automation")
@allure.feature("Authentication & Session Management")
class TestQuotesAuthentication:

    @allure.story("Test Case 6: Login Functionality and Logout Link Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc06_login_and_logout_link_validation(self, quotes_page: QuotesPage) -> None:
        quotes_page.open_homepage()
        quotes_page.click_login_link()
        quotes_page.verify_login_page_loaded()
        quotes_page.login(
            username=Config.QUOTES_USERNAME,
            password=Config.QUOTES_PASSWORD
        )
        quotes_page.verify_logged_in_state()