from uuid import uuid4

from fastapi.testclient import TestClient


def test_create_customer_returns_201(client: TestClient) -> None:
    response = client.post(
        "/customers",
        json={
            "name": "John Espitia",
            "email": f"john-{uuid4()}@example.com",
        },
    )

    assert response.status_code == 201

    body = response.json()
    assert body["name"] == "John Espitia"
    assert body["status"] == "PENDING"
    assert "id" in body
    assert "created_at" in body


def test_create_customer_rejects_duplicate_email(
    client: TestClient,
) -> None:
    email = f"duplicate-{uuid4()}@example.com"
    payload = {"name": "John", "email": email}

    first_response = client.post("/customers", json=payload)
    second_response = client.post("/customers", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_list_customers_returns_created_customer(
    client: TestClient,
) -> None:
    email = f"list-{uuid4()}@example.com"
    client.post(
        "/customers",
        json={"name": "Customer List Test", "email": email},
    )

    response = client.get("/customers")

    assert response.status_code == 200
    assert any(customer["email"] == email for customer in response.json())


def test_list_customers_filters_by_status(client: TestClient) -> None:
    email = f"pending-{uuid4()}@example.com"
    client.post(
        "/customers",
        json={"name": "Pending Customer", "email": email},
    )

    response = client.get("/customers", params={"status": "PENDING"})

    assert response.status_code == 200
    assert all(customer["status"] == "PENDING" for customer in response.json())


def test_get_customer_returns_404_for_unknown_id(
    client: TestClient,
) -> None:
    response = client.get(f"/customers/{uuid4()}")

    assert response.status_code == 404


def test_update_customer_status_persists_change(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/customers",
        json={
            "name": "Status Test",
            "email": f"status-{uuid4()}@example.com",
        },
    )
    customer_id = create_response.json()["id"]

    update_response = client.patch(
        f"/customers/{customer_id}/status",
        json={"status": "ACTIVE"},
    )

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "ACTIVE"

    get_response = client.get(f"/customers/{customer_id}")

    assert get_response.status_code == 200
    assert get_response.json()["status"] == "ACTIVE"


def test_update_customer_rejects_invalid_status(
    client: TestClient,
) -> None:
    response = client.patch(
        f"/customers/{uuid4()}/status",
        json={"status": "INVALID"},
    )

    assert response.status_code == 422
