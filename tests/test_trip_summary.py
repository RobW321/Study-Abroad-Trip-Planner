import os

from database import connection
from database.connection import initialize_database


from trips.model import Trip
from expenses.model import Expense
from trips.service import create_trip
from expenses.service import create_expense
from application.trip_summary import (
    get_trip_expenses,
    get_total_expenses,
    get_trip_summary,
)

TEST_DATABASE = "test_studytrip.db"


def create_test_trip():
    return create_trip(
        Trip(
            name="Budget Test Trip",
            destination="Madrid",
            start_date="2026-10-01",
            end_date="2026-10-07",
            planned_budget=5000.00,
        )
    )

def setup_function():
    connection.DATABASE_NAME = TEST_DATABASE
    initialize_database()


def teardown_function():
    if os.path.exists(TEST_DATABASE):
        os.remove(TEST_DATABASE)


def test_get_trip_expenses():
    trip = create_trip(
        Trip(
            name="Spain Trip",
            destination="Madrid",
            start_date="2026-10-01",
            end_date="2026-10-07",
            planned_budget=1000.00,
        )
    )

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Hotel",
            amount=100.00,
            category="Accommodation",
        )
    )

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Dinner",
            amount=25.00,
            category="Food",
        )
    )

    expenses = get_trip_expenses(trip.id)

    assert len(expenses) == 2


def test_get_total_expenses():
    trip = create_trip(
        Trip(
            name="Paris Trip",
            destination="Paris",
            start_date="2026-10-10",
            end_date="2026-10-12",
            planned_budget=800.00,
        )
    )

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Train",
            amount=50.00,
            category="Transportation",
        )
    )

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Food",
            amount=30.00,
            category="Food",
        )
    )

    assert get_total_expenses(trip.id) == 80.00


def test_get_trip_summary():
    trip = create_trip(
        Trip(
            name="Rome Trip",
            destination="Rome",
            start_date="2026-11-01",
            end_date="2026-11-05",
            planned_budget=1200.00,
        )
    )

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Museum",
            amount=20.00,
            category="Activities",
        )
    )

    summary = get_trip_summary(trip.id)

    assert summary["trip"].id == trip.id
    assert len(summary["expenses"]) == 1
    assert summary["total_expenses"] == 20.00

def test_trip_summary_calculates_remaining_budget():
    trip = create_test_trip()

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Hotel",
            amount=1200.00,
            category="Lodging",
        )
    )

    summary = get_trip_summary(trip.id)

    assert summary["total_expenses"] == 1200.00
    assert summary["remaining_budget"] == 3800.00