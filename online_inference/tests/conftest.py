import pytest

from fastapi.testclient import TestClient

from heart_diss_app import app


@pytest.fixture()
def test_client():
    return TestClient(app)
