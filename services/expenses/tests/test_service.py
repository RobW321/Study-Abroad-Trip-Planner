from unittest.mock import MagicMock

import pytest
import requests

from services.expenses import service
from services.expenses.model import Expense


def make_expense():
    return Expense(
        id=None,
        trip_id=42,
        description="Dinner in Madrid",
        amount=25.50,
        category="Food"
    )


def test_validate_expense_success():
    service.validate_expense(make_expense())


def test_validate_expense_negative_amount():
    expense = make_expense()
    expense.amount = -10

    with pytest.raises(ValueError, match="negative"):
        service.validate_expense(expense)


def test_validate_expense_empty_description():
    expense = make_expense()
    expense.description = "   "

    with pytest.raises(ValueError, match="description"):
        service.validate_expense(expense)


def test_validate_expense_empty_category():
    expense = make_expense()
    expense.category = "   "

    with pytest.raises(ValueError, match="category"):
        service.validate_expense(expense)


def test_create_expense_success(monkeypatch):
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = (101,)

    response = MagicMock()
    response.status_code = 200

    monkeypatch.setenv("TRIPS_URL", "http://trips:5001")
    monkeypatch.setattr(service.requests, "get", lambda *args, **kwargs: response)
    monkeypatch.setattr(service, "get_connection", lambda: connection)

    expense = make_expense()
    result = service.create_expense(expense)

    assert result.id == 101
    assert result.description == "Dinner in Madrid"
    connection.commit.assert_called_once()
    connection.close.assert_called_once()


def test_create_expense_trip_not_found(monkeypatch):
    response = MagicMock()
    response.status_code = 404

    monkeypatch.setenv("TRIPS_URL", "http://trips:5001")
    monkeypatch.setattr(service.requests, "get", lambda *args, **kwargs: response)

    with pytest.raises(service.TripNotFoundError):
        service.create_expense(make_expense())


def test_create_expense_trips_url_missing(monkeypatch):
    monkeypatch.delenv("TRIPS_URL", raising=False)

    with pytest.raises(service.TripsServiceUnavailableError):
        service.create_expense(make_expense())


def test_create_expense_timeout(monkeypatch):
    def timeout(*args, **kwargs):
        raise requests.exceptions.Timeout()

    monkeypatch.setenv("TRIPS_URL", "http://trips:5001")
    monkeypatch.setattr(service.requests, "get", timeout)

    with pytest.raises(service.TripsServiceTimeoutError):
        service.create_expense(make_expense())


def test_create_expense_connection_error(monkeypatch):
    def connection_error(*args, **kwargs):
        raise requests.exceptions.ConnectionError()

    monkeypatch.setenv("TRIPS_URL", "http://trips:5001")
    monkeypatch.setattr(service.requests, "get", connection_error)

    with pytest.raises(service.TripsServiceUnavailableError):
        service.create_expense(make_expense())


def test_create_expense_unexpected_status(monkeypatch):
    response = MagicMock()
    response.status_code = 500

    monkeypatch.setenv("TRIPS_URL", "http://trips:5001")
    monkeypatch.setattr(service.requests, "get", lambda *args, **kwargs: response)

    with pytest.raises(service.TripsServiceUnavailableError):
        service.create_expense(make_expense())


def test_get_expense(monkeypatch):
    connection = MagicMock()
    connection.cursor.return_value.fetchone.return_value = (
        101, 42, "Dinner in Madrid", 25.50, "Food"
    )

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    result = service.get_expense(101)

    assert result.id == 101
    assert result.trip_id == 42
    assert result.description == "Dinner in Madrid"
    connection.close.assert_called_once()


def test_get_expense_not_found(monkeypatch):
    connection = MagicMock()
    connection.cursor.return_value.fetchone.return_value = None

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    assert service.get_expense(999) is None
    connection.close.assert_called_once()


def test_get_expenses_for_trip(monkeypatch):
    connection = MagicMock()
    connection.cursor.return_value.fetchall.return_value = [
        (101, 42, "Dinner in Madrid", 25.50, "Food"),
        (102, 42, "Metro ticket", 2.00, "Transport")
    ]

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    result = service.get_expenses_for_trip(42)

    assert len(result) == 2
    assert result[0].id == 101
    assert result[1].category == "Transport"
    connection.close.assert_called_once()


def test_update_expense(monkeypatch):
    connection = MagicMock()
    monkeypatch.setattr(service, "get_connection", lambda: connection)

    service.update_expense(make_expense())

    connection.commit.assert_called_once()
    connection.close.assert_called_once()


def test_delete_expense(monkeypatch):
    connection = MagicMock()
    monkeypatch.setattr(service, "get_connection", lambda: connection)

    service.delete_expense(101)

    connection.commit.assert_called_once()
    connection.close.assert_called_once()