import os
import logging
import time

from flask import Flask, jsonify, request, g

from database.connection import initialize_database, get_connection
from .model import Trip
from .service import (
    create_trip,
    get_trip,
    get_all_trips,
    update_trip,
    delete_trip,
)


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

app.logger.setLevel(logging.INFO)


@app.before_request
def start_request_timer():
    g.start_time = time.perf_counter()


@app.after_request
def log_request(response):
    duration = (time.perf_counter() - g.start_time) * 1000

    app.logger.info(
        "%s %s %s %.2fms",
        request.method,
        request.path,
        response.status_code,
        duration,
    )

    return response


def trip_to_dict(trip):
    return {
        "id": trip.id,
        "name": trip.name,
        "destination": trip.destination,
        "start_date": trip.start_date,
        "end_date": trip.end_date,
        "planned_budget": trip.planned_budget,
    }


@app.get("/health")
def health_check():
    try:
        connection = get_connection()
        connection.execute("SELECT 1")
        connection.close()

        return jsonify({
            "status": "healthy",
            "database": "connected",
            "version": os.environ.get("SERVICE_VERSION", "dev"),
        }), 200

    except Exception:
        app.logger.exception("Database health check failed")

        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "version": os.environ.get("SERVICE_VERSION", "dev"),
        }), 503


@app.get("/trips")
def list_trips():
    trips = get_all_trips()

    return jsonify({
        "trips": [trip_to_dict(trip) for trip in trips]
    }), 200


@app.get("/trips/<int:trip_id>")
def display_trip(trip_id):
    trip = get_trip(trip_id)

    if trip is None:
        return jsonify({"error": "Trip does not exist"}), 404

    return jsonify({"trip": trip_to_dict(trip)}), 200


@app.post("/trips")
def add_trip():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "name",
        "destination",
        "start_date",
        "end_date",
        "planned_budget",
    ]

    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required trip fields"}), 400

    try:
        trip = Trip(
            name=data["name"],
            destination=data["destination"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            planned_budget=float(data["planned_budget"]),
        )

        created_trip = create_trip(trip)

        return jsonify({"trip": trip_to_dict(created_trip)}), 201

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid trip data"}), 400


@app.put("/trips/<int:trip_id>")
def edit_trip(trip_id):
    existing_trip = get_trip(trip_id)

    if existing_trip is None:
        return jsonify({"error": "Trip does not exist"}), 404

    data = request.get_json(silent=True) or {}

    try:
        existing_trip.name = data.get("name", existing_trip.name)
        existing_trip.destination = data.get(
            "destination", existing_trip.destination
        )
        existing_trip.start_date = data.get(
            "start_date", existing_trip.start_date
        )
        existing_trip.end_date = data.get(
            "end_date", existing_trip.end_date
        )
        existing_trip.planned_budget = float(
            data.get("planned_budget", existing_trip.planned_budget)
        )

        update_trip(existing_trip)

        return jsonify({"trip": trip_to_dict(existing_trip)}), 200

    except (TypeError, ValueError):
        return jsonify({"error": "Invalid trip data"}), 400


@app.delete("/trips/<int:trip_id>")
def remove_trip(trip_id):
    existing_trip = get_trip(trip_id)

    if existing_trip is None:
        return jsonify({"error": "Trip does not exist"}), 404

    delete_trip(trip_id)

    return jsonify({"message": "Trip deleted successfully"}), 200


if __name__ == "__main__":
    initialize_database()

    port = int(os.environ.get("PORT", 5001))

    app.run(host="0.0.0.0", port=port)
