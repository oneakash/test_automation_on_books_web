from playwright.sync_api import Page, Locator, expect
import allure
from pages.base_page import BasePage


class BookDetailsPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.product_main: Locator = page.locator("div.product_main")
        self.book_title_h1: Locator = page.locator("div.product_main h1")
        self.book_price: Locator = page.locator("div.product_main p.price_color")
        self.product_info_table: Locator = page.locator("table.table.table-striped")
        self.availability: Locator = page.locator("div.product_main p.instock.availability")

    @allure.step("Verify Book Details page loaded properly")
    def verify_details_page_loaded(self) -> None:
        expect(self.product_main).to_be_visible()
        expect(self.book_title_h1).to_be_visible()
        expect(self.book_price).to_be_visible()
        expect(self.product_info_table).to_be_visible()
        expect(self.availability).to_be_visible()

    @allure.step("Get Book H1 Title from Details Page")
    def get_h1_title(self) -> str:
        return self.book_title_h1.inner_text().strip()

    @allure.step("Get Book Price from Details Page")
    def get_price(self) -> str:
        return self.book_price.inner_text().strip()