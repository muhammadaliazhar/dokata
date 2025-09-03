import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tempfile
import os


# ✅ Add support for --env option
def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",   # default environment if not provided
        help="Environment to run tests against (e.g. dev, sandbox, prod)",
    )

@pytest.fixture(scope="session")
def env(request):
    """Fixture to access the environment passed via --env option."""
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def driver():
    """Setup Chrome WebDriver for Jenkins (headless, unique profile)."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")         # Headless mode for Jenkins
    chrome_options.add_argument("--no-sandbox")           # Required in CI
    chrome_options.add_argument("--disable-dev-shm-usage")# Prevent crashes
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")

    # ✅ Create unique temporary profile directory for each run
    user_data_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Optional: start maximized
    chrome_options.add_argument("--window-size=1920,1080")

    # ✅ Use webdriver-manager to auto-install matching ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    yield driver
    driver.quit()

    # cleanup temp profile
    try:
        os.rmdir(user_data_dir)
    except Exception:
        pass
