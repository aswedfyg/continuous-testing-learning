import pytest
from fastapi.testclient import TestClient

from app.main import CART_ITEMS, app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def clear_cart() -> None:
    CART_ITEMS.clear()
