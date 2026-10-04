import os
from database import connection

from database.connection import initialize_database
from trips.model import Trip
from trips.service import (
    create_trip,
    get_trip,
    get_all_trips,
    update_trip,
    delete_trip,
)


TEST_DATABASE = "test_studytrip.db"


def setup_function():
    connection.DATABASE_NAME = TEST_DATABASE
    initialize_database()


def teardown_function():
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)


def test_create_and_get_trip():
    trip = Trip(
        name="Spain Study Abroad",
        destination="Madrid",
        start_date="2026-08-31",
        end_date="2026-12-18",
        planned_budget=5000.00,
    )

    created_trip = create_trip(trip)
    retrieved_trip = get_trip(created_trip.id)

    assert created_trip.id is not None
    assert retrieved_trip.name == "Spain Study Abroad"
    assert retrieved_trip.destination == "Madrid"
    assert retrieved_trip.planned_budget == 5000.00


def test_get_all_trips():
    create_trip(
        Trip(
            name="Spain Trip",
            destination="Madrid",
            start_date="2026-08-31",
            end_date="2026-12-18",
            planned_budget=1000.00,
        )
    )

    create_trip(
        Trip(
            name="Portugal Trip",
            destination="Lisbon",
            start_date="2026-09-18",
            end_date="2026-09-21",
            planned_budget=800.00,
        )
    )

    trips = get_all_trips()

    assert len(trips) >= 2


def test_update_trip():
    trip = create_trip(
        Trip(
            name="Spain Trip",
            destination="Madrid",
            start_date="2026-08-31",
            end_date="2026-12-18",
            planned_budget=1000.00,
        )
    )

    trip.name = "Updated Spain Trip"
    trip.destination = "Barcelona"
    trip.planned_budget = 1200.00

    update_trip(trip)

    updated_trip = get_trip(trip.id)

    assert updated_trip.name == "Updated Spain Trip"
    assert updated_trip.destination == "Barcelona"
    assert updated_trip.planned_budget == 1200.00


def test_delete_trip():
    trip = create_trip(
        Trip(
            name="Temporary Trip",
            destination="Paris",
            start_date="2026-10-01",
            end_date="2026-10-05",
            planned_budget=500.00,
        )
    )

    delete_trip(trip.id)

    assert get_trip(trip.id) is None


def test_get_nonexistent_trip():
    trip = get_trip(99999)

    assert trip is None


def test_delete_nonexistent_trip():
    delete_trip(99999)

    assert get_trip(99999) is None