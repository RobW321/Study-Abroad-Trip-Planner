# Study-Abroad-Trip-Planner

A Flask and SQLite application for planning study-abroad trips and tracking their actual expenses against a planned budget.

## Overview

The Study-Abroad-Trip-Planner is a small monolithic application designed as the foundation for future DevOps work.

The application contains two distinct backend domains:

1. **Trip Planning**

   * Stores trip information.
   * Stores the planned budget for each trip.
   * Provides CRUD operations for trips.

2. **Expense Tracking**

   * Stores expenses associated with a trip.
   * Provides CRUD operations for expenses.
   * Validates expense information.

An application layer combines the two domains to provide a trip summary containing planned budget, actual spending, and remaining budget.

The application currently runs as a single Flask process backed by SQLite.

## Architecture

```text
                    Flask API
                        |
             +----------+----------+
             |                     |
          GET /              GET /trips/<id>
             |                     |
       Trip Planning       Application Layer
             |                     |
             |              +------+------+
             |              |             |
             |        Trip Planning   Expense Tracking
             |              |             |
             +--------------+-------------+
                            |
                          SQLite
```

### Trip Planning Domain

Located in:

```text
trips/
    model.py
    service.py
```

The Trip domain owns trip information and planned budgets.

### Expense Tracking Domain

Located in:

```text
expenses/
    model.py
    service.py
```

The Expense domain owns actual expense information.

### Application Layer

Located in:

```text
application/trip_summary.py
```

The application layer coordinates the two domains without moving domain-specific database logic into the other domain.

For example:

```text
Planned budget:   $5,000
Actual expenses:  $1,200
Remaining budget: $3,800
```

## Database

The application uses SQLite.

The database contains two primary tables:

### `trips`

| Column           | Description             |
| ---------------- | ----------------------- |
| `id`             | Primary key             |
| `name`           | Trip name               |
| `destination`    | Trip destination        |
| `start_date`     | Trip start date         |
| `end_date`       | Trip end date           |
| `planned_budget` | Planned spending budget |

### `expenses`

| Column        | Description                        |
| ------------- | ---------------------------------- |
| `id`          | Primary key                        |
| `trip_id`     | Foreign key referencing `trips.id` |
| `description` | Expense description                |
| `amount`      | Expense amount                     |
| `category`    | Expense category                   |

Each trip can have multiple expenses.

## Project Structure

```text
Study-Abroad-Trip-Planner/
├── application/
│   ├── __init__.py
│   └── trip_summary.py
├── database/
│   ├── __init__.py
│   ├── connection.py
│   └── db.py
├── expenses/
│   ├── __init__.py
│   ├── model.py
│   └── service.py
├── tests/
│   ├── test_database.py
│   ├── test_expenses.py
│   ├── test_trip_summary.py
│   └── test_trips.py
├── trips/
│   ├── __init__.py
│   ├── model.py
│   └── service.py
├── ADR.md
├── AI_Usage.md
├── README.md
├── app.py
└── requirements.txt
```

## Requirements

The application uses:

* Python
* Flask
* SQLite
* pytest
* pytest-cov

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Application

The application starts with:

```bash
python app.py
```

By default, Flask listens on port `5000`.

A different port can be supplied using the `PORT` environment variable:

```bash
PORT=5001 python app.py
```

The application binds to:

```text
0.0.0.0
```

so it can accept connections from a container or other host.

## Database Location

The SQLite database is stored as:

```text
studytrip.db
```

By default it is created in the current directory.

The directory can be configured using the `DATA_DIR` environment variable:

```bash
DATA_DIR=./data python app.py
```

The resulting database path is:

```text
./data/studytrip.db
```

No external database is required.

## API Endpoints

### Get all trips

```http
GET /
```

Example:

```bash
curl http://localhost:5000/
```

Example response:

```json
{
  "trips": [
    {
      "id": 1,
      "name": "Barcelona Trip",
      "destination": "Barcelona",
      "start_date": "2026-10-03",
      "end_date": "2026-10-05",
      "planned_budget": 500.0
    }
  ]
}
```

### Get a trip summary

```http
GET /trips/<trip_id>
```

Example:

```bash
curl http://localhost:5000/trips/1
```

The response includes:

* Trip information
* Planned budget
* Expenses
* Total actual expenses
* Remaining budget

For example:

```json
{
  "trip": {
    "id": 1,
    "name": "Barcelona Trip",
    "destination": "Barcelona",
    "start_date": "2026-10-03",
    "end_date": "2026-10-05",
    "planned_budget": 500.0
  },
  "expenses": [],
  "total_expenses": 0,
  "remaining_budget": 500.0
}
```

A nonexistent trip returns HTTP `404`.

## Testing

Run the complete test suite:

```bash
python -m pytest
```

The final test suite contains:

```text
21 passed
```

Run the test suite with coverage:

```bash
python -m pytest --cov=. --cov-report=term-missing
```

The final measured coverage is:

```text
96%
```

This exceeds the assignment requirement of at least 70% coverage.

Testing focuses primarily on:

* Trip business logic
* Expense business logic
* SQLite database behavior
* CRUD operations
* Invalid input and edge cases
* Cross-domain trip summaries
* Planned-budget calculations

## Architecture Decisions

The major architectural decisions are documented in `ADR.md`.

The five required decisions cover:

1. Backend language and framework
2. Domain boundaries
3. SQLite schema
4. Testing approach
5. A deliberately excluded feature

## AI Usage

AI was used during development for implementation guidance, debugging, architectural discussion, testing, and documentation.

The detailed AI interaction log is available in:

```text
AI_Usage.md
```

## Project Scope

This assignment intentionally remains a small monolithic application.

The project does **not** include:

* Docker
* Docker Compose
* CI workflows
* Infrastructure as Code
* External databases
* External caches
* Message brokers
* Background workers
* Authentication

These features are outside the scope of this assignment and can be considered in later DevOps work.
