import copy
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities dict before each test."""
    original = copy.deepcopy(app_module.activities)
    # Restore fresh copy
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
    yield
    # Ensure clean state after test as well
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))
