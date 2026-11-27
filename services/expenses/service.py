import os

import requests

from .database import get_connection
from .model import Expense


class TripNotFoundError(Exception):
    pass


class TripsServiceUnavailableError(Exception):
    pass


class TripsServiceTimeoutError(Exception):
    pass


def validate_expense(expense):
    if expense.amount < 0:
        raise ValueError("Expense amount cannot be negative")

    if not expense.description.strip():
        raise ValueError("Expense description cannot be empty")

    if not expense.category.strip():
        raise ValueError("Expense category cannot be empty")


def create_expense(expense):
    validate_expense(expense)

    trips_url = os.environ.get("TRIPS_URL", "http://trips:5001")

    if not trips_url:
        raise TripsServiceUnavailableError(
            "Trips service URL is not configured"
        )

    # Verify that the trip exists through the Trips HTTP API.
    try:
        response = requests.get(
            f"{trips_url.rstrip('/')}/trips/{expense.trip_id}",
            timeout=(2, 5),
        )

    except requests.exceptions.Timeout:
        raise TripsServiceTimeoutError(
            "Trips service request timed out"
        )

    except requests.exceptions.RequestException:
        raise TripsServiceUnavailableError(
            "Unable to communicate with Trips service"
        )

    if response.status_code == 404:
        raise TripNotFoundError("Trip does not exist")

    if response.status_code != 200:
        raise TripsServiceUnavailableError(
            "Trips service returned an unexpected response"
        )

    # Trip exists, so create the expense in ExpensesDB.
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO expenses (
                trip_id, description, amount, category
            )
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?)
            """,
            (
                expense.trip_id,
                expense.description,
                expense.amount,
                expense.category,
            ),
        )

        expense.id = cursor.fetchone()[0]
        connection.commit()

    finally:
        connection.close()

    return expense


def get_expense(expense_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, trip_id, description, amount, category
            FROM expenses
            WHERE id = ?
            """,
            (expense_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Expense(
            id=row[0],
            trip_id=row[1],
            description=row[2],
            amount=row[3],
            category=row[4],
        )

    finally:
        connection.close()


def get_expenses_for_trip(trip_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, trip_id, description, amount, category
            FROM expenses
            WHERE trip_id = ?
            """,
            (trip_id,),
        )

        rows = cursor.fetchall()

        return [
            Expense(
                id=row[0],
                trip_id=row[1],
                description=row[2],
                amount=row[3],
                category=row[4],
            )
            for row in rows
        ]

    finally:
        connection.close()


def update_expense(expense):
    validate_expense(expense)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE expenses
            SET description = ?, amount = ?, category = ?
            WHERE id = ?
            """,
            (
                expense.description,
                expense.amount,
                expense.category,
                expense.id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def delete_expense(expense_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,),
        )

        connection.commit()

    finally:
        connection.close()
