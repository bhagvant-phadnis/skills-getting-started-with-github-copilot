import copy
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Restore the in-memory `activities` dict before/after each test for isolation."""
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
