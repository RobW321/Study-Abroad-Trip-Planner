from database.connection import get_connection
from expenses.model import Expense


def validate_expense(expense):
    if expense.amount < 0:
        raise ValueError("Expense amount cannot be negative")

    if not expense.description.strip():
        raise ValueError("Expense description cannot be empty")

    if not expense.category.strip():
        raise ValueError("Expense category cannot be empty")


def create_expense(expense):
    validate_expense(expense)

    connection = get_connection()

    trip = connection.execute(
        "SELECT id FROM trips WHERE id = ?",
        (expense.trip_id,),
    ).fetchone()

    if trip is None:
        connection.close()
        raise ValueError("Trip does not exist")

    cursor = connection.execute(
        """
        INSERT INTO expenses (trip_id, description, amount, category)
        VALUES (?, ?, ?, ?)
        """,
        (
            expense.trip_id,
            expense.description,
            expense.amount,
            expense.category,
        ),
    )

    connection.commit()
    expense.id = cursor.lastrowid

    connection.close()

    return expense


def get_expense(expense_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, trip_id, description, amount, category
        FROM expenses
        WHERE id = ?
        """,
        (expense_id,),
    ).fetchone()

    connection.close()

    if row is None:
        return None

    return Expense(
        id=row[0],
        trip_id=row[1],
        description=row[2],
        amount=row[3],
        category=row[4],
    )


def get_expenses_for_trip(trip_id):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, trip_id, description, amount, category
        FROM expenses
        WHERE trip_id = ?
        """,
        (trip_id,),
    ).fetchall()

    connection.close()

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


def update_expense(expense):
    validate_expense(expense)

    connection = get_connection()

    connection.execute(
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
    connection.close()


def delete_expense(expense_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM expenses
        WHERE id = ?
        """,
        (expense_id,),
    )

    connection.commit()
    connection.close()