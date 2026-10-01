import pytest

from expenses.model import Expense
from expenses.service import validate_expense


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