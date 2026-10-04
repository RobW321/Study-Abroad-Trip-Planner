# Study-Abroad Trip Planner

A Flask and SQLite backend application for planning study-abroad trips and tracking actual expenses.


## Overview

The Study-Abroad Trip Planner helps users organize trips and compare their planned trips with their actual spending.

The application is intentionally structured around two distinct backend feature domains:

1. **Trip Planning** — manages trip information including the trip name, destination, and dates.
2. **Expense Tracking** — manages expenses associated with a specific trip, including descriptions, amounts, and categories.

The application layer combines these domains to provide a trip summary showing the expenses and total spending for a selected trip.

This separation allows each domain to be independently modularized and potentially extracted into its own service in a future architecture.


## Architecture

```text
                    Study Trip Planner
                           |
                     Application Layer
                     /               \
                    /                 \
           Trip Planning          Expense Tracking
                |                       |
          trips/service.py       expenses/service.py
                \                       /
                 \                     /
                  ------ SQLite -------
```

### Trip Planning Domain

Responsible for:

* Creating trips
* Retrieving individual trips
* Retrieving all trips
* Updating trips
* Deleting trips

### Expense Tracking Domain

Responsible for:

* Creating expenses
* Retrieving expenses
* Retrieving expenses for a trip
* Updating expenses
* Deleting expenses
* Validating expense amounts, descriptions, and categories
* Ensuring expenses reference an existing trip

### Application Layer

`application/trip_summary.py` combines the two domains.

For a selected trip, it retrieves:

* The trip
* Its associated expenses
* The total amount spent

This provides the application's main cross-domain functionality.


## Database

The application uses SQLite for persistence.

The database contains two primary tables:

### `trips`

| Column        | Type    | Description      |
| ------------- | ------- | ---------------- |
| `id`          | INTEGER | Primary key      |
| `name`        | TEXT    | Trip name        |
| `destination` | TEXT    | Trip destination |
| `start_date`  | TEXT    | Trip start date  |
| `end_date`    | TEXT    | Trip end date    |

### `expenses`

| Column        | Type    | Description           |
| ------------- | ------- | --------------------- |
| `id`          | INTEGER | Primary key           |
| `trip_id`     | INTEGER | References `trips.id` |
| `description` | TEXT    | Expense description   |
| `amount`      | REAL    | Expense amount        |
| `category`    | TEXT    | Expense category      |

Each trip can have multiple expenses through the `trip_id` foreign-key relationship.


## Project Structure

```text
Study-Abroad-Trip-Planner/
├── application/
│   └── trip_summary.py
├── database/
│   ├── connection.py
│   └── db.py
├── expenses/
│   ├── model.py
│   └── service.py
├── trips/
│   ├── model.py
│   └── service.py
├── tests/
│   ├── test_database.py
│   ├── test_expenses.py
│   ├── test_trip_summary.py
│   └── test_trips.py
├── app.py
├── ADR.md
├── README.md
└── requirements.txt
```


## Running the Application

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

The application displays the available trips and allows the user to select a trip to view its expenses and total spending.


## Running Tests

Run the test suite with:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=. --cov-report=term-missing
```

The current test suite contains **20 passing tests** and provides **87% overall code coverage**.

Testing prioritizes the core backend behavior of the Trip Planning and Expense Tracking domains, database operations, and the application-layer trip summary.


## Example Workflow

A typical workflow is:

```text
Create a trip
      ↓
Store trip in SQLite
      ↓
Add expenses associated with the trip
      ↓
Retrieve the trip and its expenses
      ↓
Calculate total spending
      ↓
Display the trip summary
```


## Architecture Decisions

Key architectural decisions are documented in `ADR.md`, including:

1. The choice of Flask/Python as the backend framework.
2. The separation of Trip Planning and Expense Tracking into distinct feature domains.
3. The SQLite schema and trip-expense relationship.
4. The testing approach and coverage priorities.
5. The deliberate exclusion of authentication and authorization from the project scope.
