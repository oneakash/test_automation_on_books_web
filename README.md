# Enterprise UI Automation Framework – Books to Scrape


## 1. Project Overview
The **Enterprise UI Automation Framework** is a production-grade end-to-end testing solution built with **Playwright** and **Pytest**. It validates functional user journeys, data consistency across pages, broken hyperlinks, image rendering attributes, pagination, authentication workflows, and mobile responsiveness across [Books to Scrape](https://books.toscrape.com/index.html) and [Quotes to Scrape](https://quotes.toscrape.com/).

---

## 2. Features
- **Page Object Model (POM) Architecture:** Clean separation between test scripts, page locators, and interaction logic.
- **SOLID & DRY Compliant:** Centralized `BasePage` methods and reusable Pytest fixtures eliminate code duplication.
- **Zero Hardcoded Waits:** Leverages Playwright's web-first assertions (`expect()`) and automatic synchronization.
- **Fast API-Level Link Checking:** Validates all page hyperlinks via Playwright's `APIRequestContext` without unnecessary browser navigation overhead.
- **Dual Reporting Engine:** Automatically generates self-contained `pytest-html` reports and rich interactive **Allure** reports.
- **Failure Diagnostics:** Captures full-page screenshots, execution videos, and Playwright traces automatically.
- **Mobile Emulation (Bonus):** Emulates iPhone 13 Pro viewports to validate responsive mobile behavior.
- **Containerized & CI/CD Ready:** Includes a production `Dockerfile` and a complete GitHub Actions pipeline.

---

## 3. Tech Stack
| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Browser Automation** | Playwright (`1.49.0`) |
| **Test Runner** | Pytest (`8.3.4`) + `pytest-playwright` |
| **Reporting** | `pytest-html` & `allure-pytest` |
| **Containerization** | Docker (`mcr.microsoft.com/playwright/python`) |
| **CI/CD** | GitHub Actions |

---

## 4. Installation Guide

### Prerequisites
- **Python 3.10+** installed on your system
- **Git** installed
- **Java JRE 8+** and **Allure CLI** (required only for viewing Allure reports locally)
- **Docker** (optional, for containerized execution)

### Step-by-Step Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/oneakash/test_automation_on_books_web.git
   cd test_automation_on_books_web
   ```
2. **Create and activate a virtual environment:**
   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Python dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. **Install Playwright browser binaries:**
   ```bash
   NODE_OPTIONS="" playwright install chromium
   ```

---

## 5. Environment Setup
All environment URLs and test constants are centrally managed in `utils/config.py`:
- `BOOKS_BASE_URL`: `https://books.toscrape.com/index.html`
- `QUOTES_BASE_URL`: `https://quotes.toscrape.com/`
- `RANDOM_SAMPLE_SIZE`: `5` (number of random books checked per run)
- `MAX_PAGINATION_PAGES`: `5` (number of paginated catalog pages validated)

No external `.env` secrets are required to run against the public sandbox targets, ensuring immediate reproducibility after cloning.

---

## 6. Running Tests

### Run All Tests (Default Headless Mode)
```bash
pytest
```

### Run in Headed Mode (Visible Browser)
```bash
pytest --headed
```

### Run Specific Test Suites or Markers
```bash
# Run only smoke tests (TC1 & TC6)
pytest -m smoke

# Run only the mobile emulation test
pytest -m mobile

# Run a single test case
pytest -k "test_tc03_book_data_consistency_validation"
```

### Run via Docker
```bash
docker build --network=host -t test_automation_on_books_web .
docker run --rm -v $(pwd)/reports:/app/reports -v $(pwd)/allure-results:/app/allure-results test_automation_on_books_web
```

---

## 7. Project Structure
```text
books-automation-framework/
├── .github/workflows/
│   └── playwright.yml          # GitHub Actions CI/CD workflow definition
├── pages/
│   ├── base_page.py            # Shared Playwright wrapper methods & assertions
│   ├── home_page.py            # Locators & methods for Books to Scrape homepage
│   ├── book_details_page.py    # Locators & methods for Book Details page
│   └── quotes_page.py          # Locators & methods for Quotes to Scrape login
├── tests/
│   ├── test_books_suite.py     # Test Cases 1–5 + Mobile Bonus test
│   └── test_quotes_login.py    # Test Case 6 (Login & Logout validation)
├── utils/
│   └── config.py               # Centralized URLs, credentials, and parameters
├── conftest.py                 # Pytest fixtures and Allure screenshot hooks
├── Dockerfile                  # Container definition for isolated execution
├── pytest.ini                  # Default Pytest CLI flags and markers
├── requirements.txt            # Locked Python package versions
└── README.md                   # Project documentation
```

---

## 8. Test Case Coverage
| ID | Test Case Name | Target Site | Description |
| :--- | :--- | :--- | :--- |
| **TC1** | Homepage Validation | Books to Scrape | Verifies URL, title, non-empty visible headings (`h1`–`h6`), and book catalog presence. |
| **TC2** | Random Book Navigation | Books to Scrape | Randomly selects 5 books, opens each details page, verifies H1 title and product table, and returns home. |
| **TC3** | Book Data Consistency | Books to Scrape | Compares homepage title and price against the details page title and price across 5 random books. |
| **TC4** | Broken Link Validation | Books to Scrape | Extracts all unique `<a href>` URLs on the homepage and verifies each returns HTTP `200`. |
| **TC5** | Product Image Validation | Books to Scrape | Validates image visibility, non-empty `src` and `alt`, and `thumbnail` class across 5 paginated pages. |
| **TC6** | Login & Logout Validation | Quotes to Scrape | Verifies login navigation, credential entry, form submission, and post-login Logout link availability. |
| **Bonus** | Mobile Device Automation | Books to Scrape | Emulates an iPhone 13 Pro viewport (`390x844`) and verifies catalog rendering and book navigation. |

---

## 9. Report Generation Guide
Both `pytest-html` and `Allure` reports are configured in `pytest.ini` to generate automatically on every test run.
- **HTML Report Output:** `reports/html/report.html`
- **Allure Raw Results Output:** `allure-results/`
- **Traces / Videos / Screenshots:** `test-results/`

---

## 10. HTML Report Guide
The HTML report is generated using `pytest-html` with the `--self-contained-html` flag so all CSS and assets are embedded in a single file.

### How to View Locally:
1. Run `pytest`.
2. Open `reports/html/report.html` directly in any web browser:
   ```bash
   # macOS
   open reports/html/report.html
   # Linux
   xdg-open reports/html/report.html
   # Windows
   start reports/html/report.html
   ```

---

## 11. Allure Report Guide
Allure provides step-by-step execution breakdowns, severity metrics, and attached failure screenshots.

### Installing Allure CLI Locally:
- **macOS (Homebrew):** `brew install allure`
- **Windows (Scoop):** `scoop install allure`
- **Linux:** Download from the [Allure GitHub Releases](https://github.com/allure-framework/allure2/releases) page.

#### In linux follow this if you don't have allure:
```
mkdir -p "$HOME/allure"
curl -sSL https://github.com/allure-framework/allure2/releases/download/2.32.0/allure-2.32.0.tgz | tar -zx -C "$HOME/allure" --strip-components=1
export PATH="$HOME/allure/bin:$PATH"
echo 'export PATH="$HOME/allure/bin:$PATH"' >> ~/.bashrc
```
#### If Fallback JAVA_HOME is not set:
```
mkdir -p "$HOME/java"
curl -sSL https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.5%2B11/OpenJDK21U-jre_x64_linux_hotspot_21.0.5_11.tar.gz | tar -zx -C "$HOME/java" --strip-components=1
export JAVA_HOME="$HOME/java"
export PATH="$JAVA_HOME/bin:$HOME/allure/bin:$PATH"
echo 'export JAVA_HOME="$HOME/java"' >> ~/.bashrc
echo 'export PATH="$JAVA_HOME/bin:$HOME/allure/bin:$PATH"' >> ~/.bashrc
```

### Viewing the Allure Report:
```bash
# Serve the report directly in your default browser
allure serve allure-results

# Or generate a standalone single-file HTML report
allure generate allure-results --clean --single-file -o allure-report
```

---

## 12. GitHub Actions Setup
The CI/CD pipeline is defined in `.github/workflows/playwright.yml`.

### Triggers
- Automatically triggers on `push` and `pull_request` events to `main`, `master`, or `develop` branches.
- Supports manual execution via `workflow_dispatch` in the GitHub Actions tab.

---

## 13. Design Decisions
1. **Handling Truncated Titles on Books to Scrape:** On the homepage, long book titles are visually truncated inside the `<a>` inner text (e.g., `"A Light in the ..."`), whereas the `title` attribute of the `<h3><a>` tag holds the full title. `HomePage.get_book_summary_by_index()` extracts the `title` attribute so exact comparisons against the details page `<h1>` never fail due to CSS/HTML truncation.
2. **Playwright `APIRequestContext` for Broken Links:** Instead of opening 50+ full browser tabs to validate links in TC4, the framework uses `page.request.get(url)`, which shares the browser context's session and executes HTTP status checks in milliseconds.
3. **Web-First Assertions:** All element checks use ` playwright.sync_api.expect` which automatically retries until the condition is met, eliminating flaky `time.sleep()` calls.

---

## 14. Known Limitations
- **Static Sandbox Target:** `books.toscrape.com` is a static sandbox site; search filter mutations or shopping cart checkouts are non-functional by design on the target website.
- **Mock Authentication on Quotes to Scrape:** `quotes.toscrape.com/login` accepts any non-empty username/password combination and does not test negative invalid-credential server errors.