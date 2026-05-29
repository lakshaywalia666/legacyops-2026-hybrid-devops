def test_create_and_list_products(client):
    payload = {
        "sku": "TEST-SKU-001",
        "name": "Test Product",
        "category": "Testing",
        "unit_price": 100.0,
        "stock_quantity": 10,
    }

    response = client.post("/products", json=payload)
    assert response.status_code in (201, 409)

    list_response = client.get("/products")
    assert list_response.status_code == 200
    assert isinstance(list_response.json(), list)
