import pytest

from database.connection import get_connection, initialize_database
from expenses.model import Expense
from expenses.service import (
    create_expense,
    delete_expense,
    get_expense,
    get_expenses_for_trip,
    update_expense,
    validate_expense,
)
from trips.model import Trip
from trips.service import create_trip


def setup_function():
    connection = get_connection()

    connection.execute("DELETE FROM expenses")
    connection.execute("DELETE FROM trips")

    connection.commit()
    connection.close()

    initialize_database()


def create_test_trip():
    return create_trip(
        Trip(
            name="Spain Study Abroad",
            destination="Madrid",
            start_date="2026-08-31",
            end_date="2026-12-18",
        )
    )

def test_valid_expense():
    expense = Expense(
        trip_id=1,
        description="Dinner",
        amount=25.50,
        category="Food",
    )

    validate_expense(expense)


def test_negative_expense_rejected():
    expense = Expense(
        trip_id=1,
        description="Dinner",
        amount=-10,
        category="Food",
    )

    with pytest.raises(ValueError):
        validate_expense(expense)


def test_empty_description_rejected():
    expense = Expense(
        trip_id=1,
        description="",
        amount=25,
        category="Food",
    )

    with pytest.raises(ValueError):
        validate_expense(expense)


def test_empty_category_rejected():
    expense = Expense(
        trip_id=1,
        description="Dinner",
        amount=25,
        category="",
    )

    with pytest.raises(ValueError):
        validate_expense(expense)


def test_create_and_get_expense():
    trip = create_test_trip()

    expense = Expense(
        trip_id=trip.id,
        description="Dinner",
        amount=25.50,
        category="Food",
    )

    created = create_expense(expense)
    retrieved = get_expense(created.id)

    assert created.id is not None
    assert retrieved.description == "Dinner"
    assert retrieved.amount == 25.50
    assert retrieved.trip_id == trip.id


def test_create_expense_requires_existing_trip():
    expense = Expense(
        trip_id=99999,
        description="Dinner",
        amount=25,
        category="Food",
    )

    with pytest.raises(ValueError):
        create_expense(expense)


def test_get_expenses_for_trip():
    trip = create_test_trip()

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Dinner",
            amount=25,
            category="Food",
        )
    )

    create_expense(
        Expense(
            trip_id=trip.id,
            description="Metro",
            amount=10,
            category="Transportation",
        )
    )

    expenses = get_expenses_for_trip(trip.id)

    assert len(expenses) == 2
    assert expenses[0].trip_id == trip.id
    assert expenses[1].trip_id == trip.id


def test_update_expense():
    trip = create_test_trip()

    expense = create_expense(
        Expense(
            trip_id=trip.id,
            description="Dinner",
            amount=25,
            category="Food",
        )
    )

    expense.description = "Restaurant dinner"
    expense.amount = 35

    update_expense(expense)

    updated = get_expense(expense.id)

    assert updated.description == "Restaurant dinner"
    assert updated.amount == 35


def test_delete_expense():
    trip = create_test_trip()

    expense = create_expense(
        Expense(
            trip_id=trip.id,
            description="Temporary expense",
            amount=20,
            category="Other",
        )
    )

    delete_expense(expense.id)

    assert get_expense(expense.id) is None