import os
import logging
import time

from flask import Flask, jsonify, request, g

from database.connection import initialize_database, get_connection
from .model import Expense
from .service import (
    create_expense,
    get_expense,
    get_expenses_for_trip,
    update_expense,
    delete_expense,
    TripNotFoundError,
    TripsServiceUnavailableError,
    TripsServiceTimeoutError,
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
        request.method, request.path, response.status_code, duration,
    )

    # Allow requests from the local frontend
    response.headers["Access-Control-Allow-Origin"] = os.environ.get(
        "UI_ORIGIN", "http://localhost:8080"
    )
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = (
        "GET, POST, PUT, DELETE, OPTIONS"
    )

    return response


def expense_to_dict(expense):
    return {
        "id": expense.id,
        "trip_id": expense.trip_id,
        "description": expense.description,
        "amount": expense.amount,
        "category": expense.category,
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


@app.get("/expenses/<int:expense_id>")
def display_expense(expense_id):
    expense = get_expense(expense_id)

    if expense is None:
        return jsonify({"error": "Expense does not exist"}), 404

    return jsonify({"expense": expense_to_dict(expense)}), 200


@app.get("/trips/<int:trip_id>/expenses")
def list_trip_expenses(trip_id):
    expenses = get_expenses_for_trip(trip_id)

    return jsonify({
        "expenses": [
            expense_to_dict(expense) for expense in expenses
        ]
    }), 200



@app.post("/expenses")
def add_expense():
    data = request.get_json(silent=True) or {}

    required_fields = [
        "trip_id",
        "description",
        "amount",
        "category",
    ]

    if any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required expense fields"}), 400

    try:
        expense = Expense(
            trip_id=int(data["trip_id"]),
            description=data["description"],
            amount=float(data["amount"]),
            category=data["category"],
        )

        created_expense = create_expense(expense)

        return jsonify({
            "expense": expense_to_dict(created_expense)
        }), 201

    except TripNotFoundError as error:
        return jsonify({"error": str(error)}), 404

    except TripsServiceTimeoutError as error:
        return jsonify({"error": str(error)}), 504

    except TripsServiceUnavailableError as error:
        return jsonify({"error": str(error)}), 503

    except ValueError as error:
        return jsonify({"error": str(error)}), 400



@app.put("/expenses/<int:expense_id>")
def edit_expense(expense_id):
    existing_expense = get_expense(expense_id)

    if existing_expense is None:
        return jsonify({"error": "Expense does not exist"}), 404

    data = request.get_json(silent=True) or {}

    try:
        existing_expense.description = data.get(
            "description", existing_expense.description
        )
        existing_expense.amount = float(
            data.get("amount", existing_expense.amount)
        )
        existing_expense.category = data.get(
            "category", existing_expense.category
        )

        update_expense(existing_expense)

        return jsonify({
            "expense": expense_to_dict(existing_expense)
        }), 200

    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.delete("/expenses/<int:expense_id>")
def remove_expense(expense_id):
    existing_expense = get_expense(expense_id)

    if existing_expense is None:
        return jsonify({"error": "Expense does not exist"}), 404

    delete_expense(expense_id)

    return jsonify({"message": "Expense deleted successfully"}), 200


if __name__ == "__main__":
    initialize_database()

    port = int(os.environ.get("PORT", 5002))

    app.run(host="0.0.0.0", port=port)
