from expenses.service import get_expenses_for_trip
from trips.service import get_trip


def get_trip_expenses(trip_id):
    return get_expenses_for_trip(trip_id)


def get_total_expenses(trip_id):
    expenses = get_expenses_for_trip(trip_id)
    return sum(expense.amount for expense in expenses)


def get_trip_summary(trip_id):
    trip = get_trip(trip_id)

    if trip is None:
        raise ValueError("Trip does not exist")

    expenses = get_expenses_for_trip(trip_id)
    total_expenses = sum(expense.amount for expense in expenses)
    remaining_budget = trip.planned_budget - total_expenses

    return {
        "trip": trip,
        "expenses": expenses,
        "total_expenses": total_expenses,
        "remaining_budget": remaining_budget,
    }