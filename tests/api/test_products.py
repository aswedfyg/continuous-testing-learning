
import pytest


def test_products_returns_expected_items(client) -> None:
    response = client.get("/products")

    assert response.status_code == 200

    products = response.json()
    assert len(products) == 3
    assert products[0] == {"id": 1, "name": "接口测试入门课", "price": 99.0}

    for product in products:
        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], float)


def test_add_product_to_cart_success(client) -> None:
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


def test_add_unknown_product_to_cart_fails(client) -> None:
    response = client.post("/cart", json={"product_id": 999, "quantity": 1})

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"



def test_add_to_cart_requires_positive_quantity(client) -> None:
    response = client.post("/cart",json={"product_id": 1, "quantity": 0})


    assert response.status_code == 422


def test_get_cart_returns_added_items(client) -> None:
    client.post("/cart", json={"product_id": 2, "quantity": 1})

    response = client.get("/cart")

    assert response.status_code == 200
    assert {
        "product_id": 2,
        "name": "UI 自动化实战课",
        "quantity": 1,
    } in response.json()


@pytest.mark.parametrize(
    ("payload", "expected_status"),
    [
        ({"product_id": 999, "quantity": 1}, 404),
        ({"product_id": 1, "quantity": 0}, 422),
        ({"product_id": 1, "quantity": -1}, 422),
    ],
)
def test_add_to_cart_invalid_payloads(payload: dict[str, int], 
                                      expected_status: int, 
                                      client) -> None:
    response = client.post("/cart", json=payload)

    assert response.status_code == expected_status


