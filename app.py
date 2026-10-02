from database.connection import initialize_database
from trips.service import get_all_trips
from application.trip_summary import get_trip_summary


def display_dashboard():
    trips = get_all_trips()

    print("\n=== Study Trip Planner ===")

    if not trips:
        print("No trips found.")
        return

    print("\nYour Trips:")

    for trip in trips:
        print(
            f"{trip.id}. {trip.name} - "
            f"{trip.destination} "
            f"({trip.start_date} to {trip.end_date})"
        )

    try:
        trip_id = int(input("\nEnter a trip ID to view: "))
    except ValueError:
        print("Invalid trip ID.")
        return

    try:
        summary = get_trip_summary(trip_id)
    except ValueError:
        print("Trip does not exist.")
        return

    trip = summary["trip"]
    expenses = summary["expenses"]
    total_expenses = summary["total_expenses"]

    print(f"\n=== {trip.name} ===")
    print(f"Destination: {trip.destination}")
    print(f"Dates: {trip.start_date} to {trip.end_date}")

    print("\nExpenses:")

    if not expenses:
        print("No expenses recorded.")
    else:
        for expense in expenses:
            print(
                f"- {expense.description}: "
                f"${expense.amount:.2f} "
                f"({expense.category})"
            )

    print(f"\nTotal Spending: ${total_expenses:.2f}")


if __name__ == "__main__":
    initialize_database()
    display_dashboard()