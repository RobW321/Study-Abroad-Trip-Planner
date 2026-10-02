from trips.model import Trip
from expenses.model import Expense
from trips.service import create_trip
from expenses.service import create_expense
from application.trip_summary import (
    get_trip_expenses,
    get_total_expenses,
    get_trip_summary,
)


def test_get_trip_expenses():
    trip = create_trip(
        Trip(
            name="Spain Trip",
            destination="Madrid",
            start_date="2026-10-01",
            end_date="2026-10-07",
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