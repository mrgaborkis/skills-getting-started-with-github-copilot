import sys
from pathlib import Path
import copy
import pytest

# Ensure repository root is on sys.path so `import src.app` works reliably
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    """Return a TestClient for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Preserve and restore the in-memory `activities` between tests.
    This runs automatically for each test to ensure isolation.
    """
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


@pytest.fixture
def sample_activity_name():
    return "Chess Club"


@pytest.fixture
def sample_email():
    return "pytest_user@example.com"
