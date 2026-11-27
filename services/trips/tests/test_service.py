from unittest.mock import MagicMock

from services.trips import service
from services.trips.model import Trip


def make_trip():
    return Trip(
        name="Spain Study Abroad",
        destination="Madrid",
        start_date="2026-08-31",
        end_date="2026-12-18",
        planned_budget=5000.00,
    )


def test_create_trip(monkeypatch):
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = (42,)

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    trip = make_trip()
    result = service.create_trip(trip)

    assert result.id == 42
    assert result.name == "Spain Study Abroad"
    connection.commit.assert_called_once()
    connection.close.assert_called_once()


def test_get_trip(monkeypatch):
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = (
        42, "Spain Study Abroad", "Madrid",
        "2026-08-31", "2026-12-18", 5000.00,
    )

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    result = service.get_trip(42)

    assert result.id == 42
    assert result.destination == "Madrid"
    connection.close.assert_called_once()


def test_get_trip_not_found(monkeypatch):
    connection = MagicMock()
    connection.cursor.return_value.fetchone.return_value = None

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    result = service.get_trip(999)

    assert result is None
    connection.close.assert_called_once()


def test_get_all_trips(monkeypatch):
    connection = MagicMock()
    connection.cursor.return_value.fetchall.return_value = [
        (42, "Spain Study Abroad", "Madrid",
         "2026-08-31", "2026-12-18", 5000.00),
        (43, "Barcelona Trip", "Barcelona",
         "2026-10-03", "2026-10-05", 500.00),
    ]

    monkeypatch.setattr(service, "get_connection", lambda: connection)

    result = service.get_all_trips()

    assert len(result) == 2
    assert result[0].id == 42
    assert result[1].destination == "Barcelona"
    connection.close.assert_called_once()


def test_update_trip(monkeypatch):
    connection = MagicMock()
    monkeypatch.setattr(service, "get_connection", lambda: connection)

    trip = make_trip()
    trip.id = 42

    service.update_trip(trip)

    connection.commit.assert_called_once()
    connection.close.assert_called_once()


def test_delete_trip(monkeypatch):
    connection = MagicMock()
    monkeypatch.setattr(service, "get_connection", lambda: connection)

    service.delete_trip(42)

    connection.commit.assert_called_once()
    connection.close.assert_called_once()
