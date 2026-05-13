from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_products_returns_expected_items() -> None:
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()
    assert len(products) == 3
    assert products[0] == {"id": 1, "name": "接口测试入门课", "price": 99.0}

    for product in products:
        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], float)


def test_add_product_to_cart_success() -> None:
    response = client.post("/cart", json={"product_id": 1, "quantity": 2})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Added to cart",
        "item": {
            "product_id": 1,
            "name": "接口测试入门课",
            "quantity": 2,
        },
    }


def test_add_unknown_product_to_cart_fails() -> None:
    response = client.post("/cart", json={"product_id": 999, "quantity": 1})

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"



def test_add_to_caryt_requires_positive_quantity() -> None:
    response = client.post("/cart",json={"product_id": 1, "quantity": 0})


    assert response.status_code == 422
