import os
import sqlite3

from .database import get_connection


def import_legacy_trips():
    legacy_path = os.environ.get("LEGACY_DB_PATH", "studytrip.db")

    # Open the original SQLite database in read-only mode.
    source = sqlite3.connect(
        f"file:{legacy_path}?mode=ro",
        uri=True,
    )

    destination = get_connection()

    try:
        source_cursor = source.cursor()
        destination_cursor = destination.cursor()

        source_cursor.execute("""
            SELECT id, name, destination, start_date,
                   end_date, planned_budget
            FROM trips
        """)

        trips = source_cursor.fetchall()

        destination_cursor.execute(
            "SELECT COUNT(*) FROM trips"
        )

        existing_count = destination_cursor.fetchone()[0]

        if existing_count > 0:
            raise RuntimeError(
                "Trips table is not empty. Aborting import."
            )

        destination_cursor.execute(
            "SET IDENTITY_INSERT trips ON"
        )

        for trip in trips:
            destination_cursor.execute("""
                INSERT INTO trips (
                    id, name, destination, start_date,
                    end_date, planned_budget
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, trip)

        destination_cursor.execute(
            "SET IDENTITY_INSERT trips OFF"
        )

        destination.commit()

        print(f"Successfully imported {len(trips)} trips.")

    except Exception:
        destination.rollback()
        raise

    finally:
        source.close()
        destination.close()


if __name__ == "__main__":
    import_legacy_trips()