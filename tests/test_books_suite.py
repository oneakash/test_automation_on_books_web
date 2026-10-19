"""Test Suite validating Books to Scrape functionality (TC1-TC5)."""

import random
import pytest
import allure
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.book_details_page import BookDetailsPage
from utils.config import Config

@allure.epic("Books to Scrape UI Automation")
@allure.feature("Core Catalog & Functional Validations")
class TestBooksToScrape:

    @allure.story("Test Case 1: Homepage Validation")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_tc01_homepage_validation(self, home_page: HomePage) -> None:
        """
        TC1: Verify that the homepage loads successfully and displays expected content.
        """
        home_page.open()
        home_page.verify_url(Config.BOOKS_BASE_URL)
        home_page.verify_title(Config.EXPECTED_BOOKS_TITLE)
        headings = home_page.get_all_visible_headings()
        assert len(headings) > 0, "Expected visible headings (h1-h6) on homepage, found 0."

        for idx, heading in enumerate(headings):
            expect(heading, f"Heading at index {idx} is not visible").to_be_visible()
            heading_text = heading.inner_text().strip()
            assert len(heading_text) > 0, f"Visible heading at index {idx} contains empty text."

        expect(home_page.books_section).to_be_visible()
        book_count = home_page.get_book_count()
        assert book_count >= 1, f"Expected at least 1 book item, but found {book_count}."

    @allure.story("Test Case 2: Random Book Navigation Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_tc02_random_book_navigation_validation(
        self, home_page: HomePage, details_page: BookDetailsPage
    ) -> None:
        """
        TC2: Randomly select 5 books and verify that each opens the correct details page.
        """
        home_page.open()
        total_books = home_page.get_book_count()
        assert total_books >= Config.RANDOM_SAMPLE_SIZE, (
            f"Not enough books ({total_books}) to sample {Config.RANDOM_SAMPLE_SIZE}."
        )

        selected_indices = random.sample(range(total_books), Config.RANDOM_SAMPLE_SIZE)

        for idx in selected_indices:
            with allure.step(f"Validating navigation for book at index {idx}"):
                book_summary = home_page.get_book_summary_by_index(idx)
                expected_title = book_summary["title"]

                home_page.click_book_by_index(idx)
                details_page.verify_details_page_loaded()

                actual_h1_title = details_page.get_h1_title()
                assert actual_h1_title == expected_title, (
                    f"H1 title mismatch! Expected '{expected_title}', got '{actual_h1_title}'."
                )

                details_page.go_back()
                home_page.verify_url(Config.BOOKS_BASE_URL)

    @allure.story("Test Case 3: Book Data Consistency Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_tc03_book_data_consistency_validation(
        self, home_page: HomePage, details_page: BookDetailsPage
    ) -> None:
        """
        TC3: Verify that book title and price on the homepage match the details page for 5 random books.
        """
        home_page.open()
        total_books = home_page.get_book_count()
        selected_indices = random.sample(range(total_books), Config.RANDOM_SAMPLE_SIZE)

        for idx in selected_indices:
            with allure.step(f"Validating data consistency for book at index {idx}"):
                homepage_data = home_page.get_book_summary_by_index(idx)
                home_title = homepage_data["title"]
                home_price = homepage_data["price"]

                home_page.click_book_by_index(idx)
                details_page.verify_details_page_loaded()

                details_title = details_page.get_h1_title()
                details_price = details_page.get_price()

                assert home_title == details_title, (
                    f"Title mismatch! Homepage: '{home_title}' vs Details: '{details_title}'"
                )
                assert home_price == details_price, (
                    f"Price mismatch for '{home_title}'! Homepage: '{home_price}' vs Details: '{details_price}'"
                )

                details_page.go_back()
                home_page.verify_url(Config.BOOKS_BASE_URL)

    @allure.story("Test Case 4: Broken Link Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_tc04_broken_link_validation(self, home_page: HomePage) -> None:
        """
        TC4: Verify that all hyperlinks on the homepage return a 200 status code.
        """
        home_page.open()
        unique_urls = home_page.get_unique_links()
        assert len(unique_urls) > 0, "No hyperlinks extracted from homepage."

        broken_links = []
        api_request_context = home_page.page.request

        for url in unique_urls:
            with allure.step(f"Checking HTTP status for URL: {url}"):
                response = api_request_context.get(url)
                if response.status != 200:
                    broken_links.append(f"{url} (Status: {response.status})")

        assert len(broken_links) == 0, f"Broken links detected: {broken_links}"

    @allure.story("Test Case 5: Product Image & Pagination Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_tc05_product_image_validation_across_pages(self, home_page: HomePage) -> None:
        """
        TC5: Verify that product images are displayed correctly across all pages.
        """
        home_page.open()
        pages_visited = 0
        while pages_visited < Config.MAX_PAGINATION_PAGES:
            pages_visited += 1
            with allure.step(f"Validating product images on Page {pages_visited}"):
                home_page.validate_product_images_on_page()

            if pages_visited < Config.MAX_PAGINATION_PAGES:
                has_next = home_page.go_to_next_page()
                if not has_next:
                    break

        assert pages_visited == Config.MAX_PAGINATION_PAGES, (
            f"Expected to validate {Config.MAX_PAGINATION_PAGES} pages, but stopped at {pages_visited}."
        )

    @allure.story("Mobile Device Automation Validation")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.mobile
    @pytest.mark.regression
    def test_bonus_mobile_viewport_homepage_and_navigation(self, mobile_page: Page) -> None:
        """
        Bonus Test: Verify that the mobile viewport is correctly applied and that navigation works as expected.
        """

        mobile_home = HomePage(mobile_page)
        mobile_details = BookDetailsPage(mobile_page)
        
        mobile_home.open()
        assert mobile_page.viewport_size["width"] == 390, "Mobile viewport width not applied properly."

        expect(mobile_home.books_section).to_be_visible()
        book_summary = mobile_home.get_book_summary_by_index(0)

        mobile_home.click_book_by_index(0)
        mobile_details.verify_details_page_loaded()
        assert mobile_details.get_h1_title() == book_summary["title"]