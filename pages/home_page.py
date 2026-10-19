from typing import List, Dict
from urllib.parse import urljoin
from playwright.sync_api import Page, Locator, expect
import allure
from pages.base_page import BasePage
from utils.config import Config


class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.books_section: Locator = page.locator("section")
        self.book_cards: Locator = page.locator("article.product_pod")
        self.visible_headings: Locator = page.locator("h1:visible, h2:visible, h3:visible, h4:visible, h5:visible, h6:visible")
        self.anchor_tags: Locator = page.locator("a[href]")
        self.product_images: Locator = page.locator("article.product_pod div.image_container img")
        self.next_button: Locator = page.locator("li.next a")

    @allure.step("Open Books to Scrape Homepage")
    def open(self) -> None:
        """Navigates directly to the Books to Scrape homepage."""
        self.navigate(Config.BOOKS_BASE_URL)

    @allure.step("Get all visible headings (h1-h6)")
    def get_all_visible_headings(self) -> List[Locator]:
        """Returns a list of locators for all visible h1-h6 headings."""
        return self.visible_headings.all()

    @allure.step("Get count of books displayed on current page")
    def get_book_count(self) -> int:
        """Returns the number of book cards displayed on the current page."""
        return self.book_cards.count()

    @allure.step("Extract title and price for book at index {index}")
    def get_book_summary_by_index(self, index: int) -> Dict[str, str]:
        """
        Extracts the full book title
        and price text from a specific book card on the homepage.
        """
        card = self.book_cards.nth(index)
        title_link = card.locator("h3 a")
        full_title = title_link.get_attribute("title") or title_link.inner_text()
        price = card.locator("p.price_color").inner_text().strip()
        return {"title": full_title.strip(), "price": price}

    @allure.step("Click on book at index {index}")
    def click_book_by_index(self, index: int) -> None:
        """Clicks the title link of the book at the specified index."""
        card = self.book_cards.nth(index)
        card.locator("h3 a").click()

    @allure.step("Extract all unique, absolute URLs from anchor tags on the page")
    def get_unique_links(self) -> List[str]:
        """Extracts all href values, resolves relative paths, and removes duplicates."""
        base_url = self.get_current_url()
        links = set()
        for anchor in self.anchor_tags.all():
            href = anchor.get_attribute("href")
            if href and not href.startswith(("javascript:", "mailto:", "#")):
                absolute_url = urljoin(base_url, href)
                links.add(absolute_url)
        return list(links)

    @allure.step("Validate all product images on current page")
    def validate_product_images_on_page(self) -> None:
        """Asserts visibility, non-empty src/alt attributes, and 'thumbnail' class on all product images."""
        images = self.product_images.all()
        assert len(images) > 0, "No product images found on the current page."

        for idx, img in enumerate(images):
            expect(img, f"Image at index {idx} is not visible").to_be_visible()

            src = img.get_attribute("src")
            assert src and src.strip() != "", f"Image at index {idx} has missing or empty 'src' attribute."

            alt = img.get_attribute("alt")
            assert alt and alt.strip() != "", f"Image at index {idx} has missing or empty 'alt' attribute."

            class_attr = img.get_attribute("class")
            assert class_attr and "thumbnail" in class_attr.split(), (
                f"Image at index {idx} class '{class_attr}' does not contain 'thumbnail'."
            )

    @allure.step("Click Next pagination button if available")
    def go_to_next_page(self) -> bool:
        """Clicks the Next pagination button if visible. Returns True if navigated, False otherwise."""
        if self.next_button.is_visible():
            self.next_button.click()
            self.page.wait_for_load_state("domcontentloaded")
            return True
        return False