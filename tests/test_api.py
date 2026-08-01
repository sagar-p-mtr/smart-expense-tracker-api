from __future__ import annotations

from fastapi.testclient import TestClient
import pytest

from src.main import app
from src.routes import get_storage
from src.storage import ExpenseStorage


@pytest.fixture()
def storage(tmp_path):
    return ExpenseStorage(tmp_path / "expenses.json")


@pytest.fixture()
def client(storage: ExpenseStorage):
    app.dependency_overrides[get_storage] = lambda: storage
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def make_payload(
    title: str = "Lunch",
    amount: float = 12.5,
    category: str = "Food",
    date: str = "2026-07-31",
) -> dict[str, str | float]:
    return {
        "title": title,
        "amount": amount,
        "category": category,
        "date": date,
    }


def test_add_expense(client: TestClient):
    response = client.post("/expenses", json=make_payload())

    assert response.status_code == 201
    body = response.json()
    assert "id" in body
    assert body["title"] == "Lunch"
    assert body["amount"] == 12.5
    assert body["category"] == "Food"
    assert body["date"] == "2026-07-31"


def test_get_all_expenses(client: TestClient):
    client.post("/expenses", json=make_payload(title="Lunch"))
    client.post("/expenses", json=make_payload(title="Train", category="Travel", amount=8.0))

    response = client.get("/expenses")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    titles = {item["title"] for item in body}
    assert titles == {"Lunch", "Train"}


def test_filter_by_category_is_case_insensitive(client: TestClient):
    client.post("/expenses", json=make_payload(title="Lunch", category="Food"))
    client.post("/expenses", json=make_payload(title="Coffee", category="food", amount=4.0))
    client.post("/expenses", json=make_payload(title="Taxi", category="Travel", amount=20.0))

    response = client.get("/expenses", params={"category": "FOOD"})

    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert {item["title"] for item in body} == {"Lunch", "Coffee"}


def test_total_calculation_overall_and_by_category(client: TestClient):
    client.post("/expenses", json=make_payload(title="Lunch", amount=10.0, category="Food"))
    client.post("/expenses", json=make_payload(title="Dinner", amount=15.5, category="Food"))
    client.post("/expenses", json=make_payload(title="Taxi", amount=20.0, category="Travel"))

    total_response = client.get("/expenses/total")
    food_total_response = client.get("/expenses/total", params={"category": "food"})

    assert total_response.status_code == 200
    assert total_response.json() == {"total": 45.5}

    assert food_total_response.status_code == 200
    assert food_total_response.json() == {"category": "food", "total": 25.5}


def test_delete_expense(client: TestClient):
    create_response = client.post("/expenses", json=make_payload())
    expense_id = create_response.json()["id"]

    delete_response = client.delete(f"/expenses/{expense_id}")
    all_response = client.get("/expenses")

    assert delete_response.status_code == 204
    assert delete_response.text == ""
    assert all_response.json() == []


def test_invalid_input_returns_validation_error(client: TestClient):
    invalid_payload = make_payload(title="   ", amount=-1.0, category="", date="not-a-date")

    response = client.post("/expenses", json=invalid_payload)

    assert response.status_code == 422
    detail = response.json().get("detail", [])
    assert detail


def test_missing_expense_returns_404(client: TestClient):
    response = client.delete("/expenses/96ea76a0-5a2f-46af-8a5c-e8f6b7906ad1")

    assert response.status_code == 404
    assert response.json() == {"detail": "Expense not found"}


def test_empty_storage_returns_empty_list_and_zero_total(client: TestClient):
    expenses_response = client.get("/expenses")
    total_response = client.get("/expenses/total")

    assert expenses_response.status_code == 200
    assert expenses_response.json() == []

    assert total_response.status_code == 200
    assert total_response.json() == {"total": 0}
