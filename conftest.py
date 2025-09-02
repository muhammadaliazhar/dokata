import pytest
import json
import os

def pytest_addoption(parser):
    """Add command-line option for selecting environment."""
    parser.addoption(
        "--env",
        action="store",
        default="sandbox",
        help="Environment to run tests against (e.g., sandbox, production)"
    )

@pytest.fixture(scope="session")
def config(request):
    """Load environment-specific configuration from config.json."""
    env = request.config.getoption("--env")
    config_file_path = os.path.join(os.path.dirname(__file__), "config", "config.json")

    if not os.path.exists(config_file_path):
        # Fallback for Jenkins (no config.json present)
        print(f"[WARN] config.json not found at {config_file_path}, using default values for env '{env}'.")
        return {"base_url": "http://localhost", "browser": "chrome"}

    with open(config_file_path, "r") as config_file:
        config_data = json.load(config_file)

    if env not in config_data:
        raise ValueError(f"Environment '{env}' not found in config.json!")

    return config_data[env]
