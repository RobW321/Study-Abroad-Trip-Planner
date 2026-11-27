from unittest.mock import MagicMock

from services.expenses import app as expenses_app
from services.expenses.model import Expense
from services.expenses.service import (
    TripNotFoundError,
    TripsServiceTimeoutError,
    TripsServiceUnavailableError,
)


def setup_function():
    expenses_app.app.config["TESTING"] = True


def make_expense():
    return Expense(
        id=101,
        trip_id=42,
        description="Dinner in Madrid",
        amount=25.50,
        category="Food",
    )


def test_health_success(monkeypatch):
    connection = MagicMock()
    monkeypatch.setattr(expenses_app, "get_connection", lambda: connection)

    response = expenses_app.app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"
    connection.close.assert_called_once()


def test_health_failure(monkeypatch):
    def raise_error():
        raise RuntimeError("Database unavailable")

    monkeypatch.setattr(expenses_app, "get_connection", raise_error)

    response = expenses_app.app.test_client().get("/health")

    assert response.status_code == 503
    assert response.get_json()["status"] == "unhealthy"


def test_get_expense_found(monkeypatch):
    monkeypatch.setattr(
        expenses_app, "get_expense", lambda expense_id: make_expense()
    )

    response = expenses_app.app.test_client().get("/expenses/101")

    assert response.status_code == 200
    assert response.get_json()["expense"]["id"] == 101


def test_get_expense_not_found(monkeypatch):
    monkeypatch.setattr(expenses_app, "get_expense", lambda expense_id: None)

    response = expenses_app.app.test_client().get("/expenses/999")

    assert response.status_code == 404


def test_list_trip_expenses(monkeypatch):
    monkeypatch.setattr(
        expenses_app,
        "get_expenses_for_trip",
        lambda trip_id: [make_expense()],
    )

    response = expenses_app.app.test_client().get("/trips/42/expenses")

    assert response.status_code == 200
    assert len(response.get_json()["expenses"]) == 1
    assert response.get_json()["expenses"][0]["trip_id"] == 42


def test_create_expense_success(monkeypatch):
    def create(expense):
        expense.id = 101
        return expense

    monkeypatch.setattr(expenses_app, "create_expense", create)

    response = expenses_app.app.test_client().post(
        "/expenses",
        json={
            "trip_id": 42,
            "description": "Dinner in Madrid",
            "amount": 25.50,
            "category": "Food",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["expense"]["id"] == 101


def test_create_expense_missing_fields():
    response = expenses_app.app.test_client().post(
        "/expenses",
        json={"trip_id": 42},
    )

    assert response.status_code == 400


def test_create_expense_trip_not_found(monkeypatch):
    def raise_error(expense):
        raise TripNotFoundError("Trip does not exist")

    monkeypatch.setattr(expenses_app, "create_expense", raise_error)

    response = expenses_app.app.test_client().post(
        "/expenses",
        json={
            "trip_id": 999,
            "description": "Dinner",
            "amount": 25,
            "category": "Food",
        },
    )

    assert response.status_code == 404


def test_create_expense_service_unavailable(monkeypatch):
    def raise_error(expense):
        raise TripsServiceUnavailableError("Trips service unavailable")

    monkeypatch.setattr(expenses_app, "create_expense", raise_error)

    response = expenses_app.app.test_client().post(
        "/expenses",
        json={
            "trip_id": 42,
            "description": "Dinner",
            "amount": 25,
            "category": "Food",
        },
    )

    assert response.status_code == 503


def test_create_expense_timeout(monkeypatch):
    def raise_error(expense):
        raise TripsServiceTimeoutError("Trips service timed out")

    monkeypatch.setattr(expenses_app, "create_expense", raise_error)

    response = expenses_app.app.test_client().post(
        "/expenses",
        json={
            "trip_id": 42,
            "description": "Dinner",
            "amount": 25,
            "category": "Food",
        },
    )

    assert response.status_code == 504


def test_create_expense_invalid_amount():
    response = expenses_app.app.test_client().post(
        "/expenses",
        json={
            "trip_id": 42,
            "description": "Dinner",
            "amount": -10,
            "category": "Food",
        },
    )

    assert response.status_code == 400


def test_update_expense_success(monkeypatch):
    expense = make_expense()
    monkeypatch.setattr(
        expenses_app, "get_expense", lambda expense_id: expense
    )

    updated = []
    monkeypatch.setattr(
        expenses_app,
        "update_expense",
        lambda expense: updated.append(expense),
    )

    response = expenses_app.app.test_client().put(
        "/expenses/101",
        json={"description": "Updated dinner", "amount": 30},
    )

    assert response.status_code == 200
    assert response.get_json()["expense"]["description"] == "Updated dinner"
    assert len(updated) == 1


def test_update_expense_not_found(monkeypatch):
    monkeypatch.setattr(expenses_app, "get_expense", lambda expense_id: None)

    response = expenses_app.app.test_client().put(
        "/expenses/999",
        json={"description": "Updated dinner"},
    )

    assert response.status_code == 404


def test_update_expense_invalid_amount(monkeypatch):
    expense = make_expense()
    monkeypatch.setattr(
        expenses_app, "get_expense", lambda expense_id: expense
    )

    response = expenses_app.app.test_client().put(
        "/expenses/101",
        json={"amount": -10},
    )

    assert response.status_code == 400


def test_delete_expense_success(monkeypatch):
    monkeypatch.setattr(
        expenses_app, "get_expense", lambda expense_id: make_expense()
    )

    deleted = []
    monkeypatch.setattr(
        expenses_app,
        "delete_expense",
        lambda expense_id: deleted.append(expense_id),
    )

    response = expenses_app.app.test_client().delete("/expenses/101")

    assert response.status_code == 200
    assert deleted == [101]


def test_delete_expense_not_found(monkeypatch):
    monkeypatch.setattr(expenses_app, "get_expense", lambda expense_id: None)

    response = expenses_app.app.test_client().delete("/expenses/999")

    assert response.status_code == 404