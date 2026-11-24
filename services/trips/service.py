
from .database import get_connection
from .model import Trip


def create_trip(trip):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO trips (
                name, destination, start_date, end_date, planned_budget
            )
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                trip.name,
                trip.destination,
                trip.start_date,
                trip.end_date,
                trip.planned_budget,
            ),
        )

        trip.id = cursor.fetchone()[0]
        connection.commit()

        return trip

    finally:
        connection.close()


def get_trip(trip_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, destination, start_date, end_date, planned_budget
            FROM trips
            WHERE id = ?
            """,
            (trip_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return Trip(
            id=row[0],
            name=row[1],
            destination=row[2],
            start_date=row[3],
            end_date=row[4],
            planned_budget=row[5],
        )

    finally:
        connection.close()


def get_all_trips():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, destination, start_date, end_date, planned_budget
            FROM trips
            """
        )

        rows = cursor.fetchall()

        return [
            Trip(
                id=row[0],
                name=row[1],
                destination=row[2],
                start_date=row[3],
                end_date=row[4],
                planned_budget=row[5],
            )
            for row in rows
        ]

    finally:
        connection.close()


def update_trip(trip):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE trips
            SET name = ?, destination = ?, start_date = ?, end_date = ?,
                planned_budget = ?
            WHERE id = ?
            """,
            (
                trip.name,
                trip.destination,
                trip.start_date,
                trip.end_date,
                trip.planned_budget,
                trip.id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def delete_trip(trip_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM trips
            WHERE id = ?
            """,
            (trip_id,),
        )

        connection.commit()

    finally:
        connection.close()
