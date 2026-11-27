from unittest.mock import MagicMock

from services.trips import app as trips_app


def setup_function():
    trips_app.app.config["TESTING"] = True


def test_health_success(monkeypatch):
    connection = MagicMock()
    monkeypatch.setattr(trips_app, "get_connection", lambda: connection)

    response = trips_app.app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"
    connection.close.assert_called_once()


def test_health_failure(monkeypatch):
    def raise_error():
        raise RuntimeError("Database unavailable")

    monkeypatch.setattr(trips_app, "get_connection", raise_error)

    response = trips_app.app.test_client().get("/health")

    assert response.status_code == 503
    assert response.get_json()["status"] == "unhealthy"


def test_get_all_trips(monkeypatch):
    monkeypatch.setattr(trips_app, "get_all_trips", list)

    response = trips_app.app.test_client().get("/trips")

    assert response.status_code == 200
    assert response.get_json() == {"trips": []}


def test_get_trip_found(monkeypatch):
    from services.trips.model import Trip

    trip = Trip(
        id=42,
        name="Spain Study Abroad",
        destination="Madrid",
        start_date="2026-08-31",
        end_date="2026-12-18",
        planned_budget=5000.00
    )

    monkeypatch.setattr(trips_app, "get_trip", lambda trip_id: trip)

    response = trips_app.app.test_client().get("/trips/42")

    assert response.status_code == 200
    assert response.get_json()["trip"]["id"] == 42
    assert response.get_json()["trip"]["destination"] == "Madrid"


def test_get_trip_not_found(monkeypatch):
    monkeypatch.setattr(trips_app, "get_trip", lambda trip_id: None)

    response = trips_app.app.test_client().get("/trips/999")

    assert response.status_code == 404


def test_create_trip(monkeypatch):
    def create(trip):
        trip.id = 42
        return trip

    monkeypatch.setattr(trips_app, "create_trip", create)

    response = trips_app.app.test_client().post(
        "/trips",
        json={
            "name": "Spain Study Abroad",
            "destination": "Madrid",
            "start_date": "2026-08-31",
            "end_date": "2026-12-18",
            "planned_budget": 5000
        }
    )

    assert response.status_code == 201
    assert response.get_json()["trip"]["id"] == 42


def test_create_trip_missing_fields():
    response = trips_app.app.test_client().post(
        "/trips",
        json={"name": "Incomplete trip"}
    )

    assert response.status_code == 400


def test_update_trip_not_found(monkeypatch):
    monkeypatch.setattr(trips_app, "get_trip", lambda trip_id: None)

    response = trips_app.app.test_client().put(
        "/trips/999",
        json={"name": "Updated trip"}
    )

    assert response.status_code == 404


def test_delete_trip(monkeypatch):
    from services.trips.model import Trip

    trip = Trip(
        id=42,
        name="Spain Study Abroad",
        destination="Madrid",
        start_date="2026-08-31",
        end_date="2026-12-18",
        planned_budget=5000.00
    )

    monkeypatch.setattr(trips_app, "get_trip", lambda trip_id: trip)

    deleted = []
    monkeypatch.setattr(
        trips_app,
        "delete_trip",
        lambda trip_id: deleted.append(trip_id)
    )

    response = trips_app.app.test_client().delete("/trips/42")

    assert response.status_code == 200
    assert deleted == [42]