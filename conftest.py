import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import pytest


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver in Jenkins headless environment"""
    options = Options()
    options.add_argument("--headless=new")  # use Chrome headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # give each session a unique temp profile
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver
    driver.quit()
