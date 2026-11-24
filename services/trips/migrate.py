
from pathlib import Path

from .database import get_connection


MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def run_migrations():
    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Track which migrations have already been applied.
        cursor.execute("""
            IF OBJECT_ID('schema_migrations', 'U') IS NULL
            BEGIN
                CREATE TABLE schema_migrations (
                    version NVARCHAR(255) PRIMARY KEY,
                    applied_at DATETIME2 NOT NULL
                        DEFAULT SYSUTCDATETIME()
                );
            END
        """)

        connection.commit()

        migration_files = sorted(MIGRATIONS_DIR.glob("V*__*.sql"))

        for migration_file in migration_files:
            version = migration_file.name

            cursor.execute(
                "SELECT version FROM schema_migrations WHERE version = ?",
                (version,),
            )

            if cursor.fetchone():
                print(f"Skipping already applied migration: {version}")
                continue

            sql = migration_file.read_text(encoding="utf-8")

            print(f"Applying migration: {version}")

            try:
                cursor.execute(sql)

                cursor.execute(
                    """
                    INSERT INTO schema_migrations (version)
                    VALUES (?)
                    """,
                    (version,),
                )

                connection.commit()

            except Exception:
                connection.rollback()
                raise

        print("Trips database migrations completed.")

    finally:
        connection.close()


if __name__ == "__main__":
    run_migrations()
