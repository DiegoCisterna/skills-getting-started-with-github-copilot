"""Shared pytest fixtures for the backend test suite."""
import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as app_activities


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities database before and after each test.

    The activities dict is module-level global state, so tests that mutate
    it (e.g. signing up a student) could otherwise leak into other tests.
    """
    original = copy.deepcopy(app_activities)
    yield
    app_activities.clear()
    app_activities.update(original)
