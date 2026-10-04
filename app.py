import os

from flask import Flask, jsonify

from database.connection import initialize_database
from trips.service import get_all_trips
from application.trip_summary import get_trip_summary


app = Flask(__name__)


@app.get("/")
def display_dashboard():
    trips = get_all_trips()

    return jsonify({
        "trips": [
            {
                "id": trip.id,
                "name": trip.name,
                "destination": trip.destination,
                "start_date": trip.start_date,
                "end_date": trip.end_date,
                "planned_budget": trip.planned_budget,
            }
            for trip in trips
        ]
    })


@app.get("/trips/<int:trip_id>")
def display_trip(trip_id):
    try:
        summary = get_trip_summary(trip_id)
    except ValueError:
        return jsonify({"error": "Trip does not exist"}), 404

    trip = summary["trip"]

    return jsonify({
        "trip": {
            "id": trip.id,
            "name": trip.name,
            "destination": trip.destination,
            "start_date": trip.start_date,
            "end_date": trip.end_date,
            "planned_budget": trip.planned_budget,
        },
        "expenses": [
            {
                "description": expense.description,
                "amount": expense.amount,
                "category": expense.category,
            }
            for expense in summary["expenses"]
        ],
        "total_expenses": summary["total_expenses"],
        "remaining_budget": summary["remaining_budget"],
    })


if __name__ == "__main__":
    initialize_database()

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)