"""Centralized configuration and constants for the automation framework."""

class Config:
    BOOKS_BASE_URL = "https://books.toscrape.com/index.html"
    QUOTES_BASE_URL = "https://quotes.toscrape.com/"
    EXPECTED_BOOKS_TITLE = "All products | Books to Scrape - Sandbox"
    RANDOM_SAMPLE_SIZE = 5
    MAX_PAGINATION_PAGES = 5
    
    # Valid test credentials for Quotes to Scrape (accepts any non-empty credentials)
    QUOTES_USERNAME = "enterprise_qa_user"
    QUOTES_PASSWORD = "SecurePassword123!"