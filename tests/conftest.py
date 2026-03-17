from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

ACTIVITIES_SNAPSHOT = deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: restore in-memory data to a known state before each test.
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ACTIVITIES_SNAPSHOT))


@pytest.fixture()
def client():
    # Arrange: provide a FastAPI test client for endpoint calls.
    return TestClient(app_module.app)
