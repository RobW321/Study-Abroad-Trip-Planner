from database.connection import get_connection
from trips.model import Trip


def create_trip(trip):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO trips (
            name, destination, start_date, end_date, planned_budget
        )
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

    connection.commit()
    trip.id = cursor.lastrowid

    connection.close()

    return trip


def get_trip(trip_id):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT id, name, destination, start_date, end_date, planned_budget
        FROM trips
        WHERE id = ?
        """,
        (trip_id,),
    ).fetchone()

    connection.close()

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


def get_all_trips():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, name, destination, start_date, end_date, planned_budget
        FROM trips
        """
    ).fetchall()

    connection.close()

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


def update_trip(trip):
    connection = get_connection()

    connection.execute(
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
    connection.close()


def delete_trip(trip_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM trips
        WHERE id = ?
        """,
        (trip_id,),
    )

    connection.commit()
    connection.close()