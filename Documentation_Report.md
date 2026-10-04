# Study-Abroad-Trip-Planner

## DevOps Assignment 1 Report

### 1. Project Overview

The Study-Abroad-Trip-Planner is a small monolithic web application designed to provide the foundation for future DevOps work. The application allows a user to organize study-abroad trips, define a planned budget for each trip, record actual expenses, and compare planned spending with actual spending.

The application was intentionally designed as a single-process Flask application backed by SQLite. This matches the scope of the first assignment while leaving a clear path for future containerization, deployment, and service decomposition.

The application contains two distinct backend domains: Trip Planning and Expense Tracking. Trip Planning owns trip information and planned budgets, while Expense Tracking owns actual expenses. An application layer combines information from both domains to calculate a trip's total expenses and remaining budget.

The final implementation contains 21 automated tests and achieves 96% code coverage, exceeding the assignment's 70% minimum requirement.

---

# 2. Software Development Life Cycle

## SDLC Model

The project followed an iterative Agile-inspired development process.

Rather than attempting to design and implement the entire application at once, development was divided into small increments. Each increment introduced a meaningful piece of functionality, followed by testing, documentation, and a Git commit.

The development progression was:

Initial structure
      ↓
SQLite database
      ↓
Trip domain
      ↓
Expense domain
      ↓
Application/service layer
      ↓
Testing and edge cases
      ↓
Documentation
      ↓
Flask API
      ↓
Budget comparison feature
      ↓
Final testing and documentation


Git branches and commits provided evidence of this incremental process.

## Why This Model Was Appropriate

An iterative process was appropriate because the assignment required both a working application and evidence of the development process. Building the project incrementally would reduce the risk of implementing a large amount of code before discovering architectural or testing problems.

The project also had requirements that became clearer as implementation progressed. For example, the original interactive application did not satisfy the assignment's eventual container contract. Converting the application to Flask after identifying that requirement was easier because the underlying Trip, Expense, and application services had already been separated.

This allowed the architecture to evolve without requiring the entire application to be rewritten.

## Following and Deviating from the Plan

The project generally followed the planned progression of database setup, domain implementation, testing, documentation, and application integration.

One significant adjustment was converting the original interactive command-line application into a Flask API. The original version used `input()` and interactive startup, which did not satisfy the application's eventual runtime contract. The Flask conversion removed interactive input and introduced:

* A single application process
* `python app.py` as the startup command
* `PORT` environment-variable configuration
* Binding to `0.0.0.0`

---

# 3. SMART Goals

The project was guided by several SMART goals.

### Goal 1 — Build two independent backend domains

**Specific:** Implement separate Trip Planning and Expense Tracking domains.

**Measurable:** Each domain would have its own model and service layer and would manage its own responsibilities.

**Achievable:** Both domains use the same SQLite database while remaining logically separated.

**Relevant:** This directly satisfies the requirement for two backend domains that could potentially become future microservices.

**Time-bound:** Complete during the specified time period

This goal was achieved through the `trips/` and `expenses/` packages.

### Goal 2 — Achieve reliable automated testing

**Specific:** Test the core business logic of both domains and achieve at least 70% code coverage.

**Measurable:** The final result was:

21 tests passed
92% coverage

The project therefore exceeded the required testing threshold.

**Achievable:** The project was able to reach the required testing coverage threshold

**Relevant:** This directly satisfies the requirement for sufficient testing and validation

**Time-bound:** The testing was to be completed along with the rest of the application

### Goal 3 — Create a container-compatible application

**Specific:** Ensure the application can later be started in a container using one command without interactive setup.

**Measurable:** We can track that the application can be started with one command: python app.py

**Achievable:** The application is capable of being run as a single process in a single container

**Relevant:** The application binds to `0.0.0.0`, reads its port from an environment variable, and uses SQLite without requiring an external runtime service.

**Time-bound:** This goal was planned to be completed within the scope of the project.

---

# 4. Architecture

The final architecture is a small monolithic application organized into domain-oriented modules.

```text
                         Flask API
                            |
                 +----------+----------+
                 |                     |
              GET /             GET /trips/<id>
                 |                     |
          Trip Planning          Application Layer
                 |                     |
                 |              +------+------+
                 |              |             |
                 |         Trip Planning   Expense Tracking
                 |              |             |
                 +--------------+-------------+
                                |
                              SQLite
```

## Trip Planning Domain

The Trip Planning domain is located in:

trips/model.py
trips/service.py


The model represents a trip using:

* ID
* Name
* Destination
* Start date
* End date
* Planned budget

The service layer performs database operations for creating, retrieving, updating, and deleting trips.

The domain is responsible for trip-specific data and behavior rather than expense-specific behavior.

## Expense Tracking Domain

The Expense Tracking domain is located in:

expenses/model.py
expenses/service.py


An expense contains:

* ID
* Trip ID
* Description
* Amount
* Category

The service layer handles expense persistence and validation.

The Expense domain does not own trip planning logic. It only uses the trip identifier to associate an expense with a trip.

## Application Layer

The application layer is located in:

application/trip_summary.py


This layer is responsible for combining information from the two domains.

For example:

Trip Planning
planned_budget = $5,000

        -

Expense Tracking
total_expenses = $1,200

        ↓

Application Layer
remaining_budget = $3,800


This separation is important for future service decomposition. The Trip Planning and Expense Tracking domains can eventually be extracted into separate services while an API or orchestration layer coordinates their interaction.

---

# 5. Database Design

SQLite is used as the application's persistent data store.

The database contains two primary tables.

```text
+----------------------------+
|           trips            |
+----------------------------+
| id             PK          |
| name                       |
| destination                |
| start_date                 |
| end_date                   |
| planned_budget             |
+-------------+--------------+
              |
              | 1
              |
              | many
              |
+-------------v--------------+
|          expenses          |
+----------------------------+
| id             PK          |
| trip_id        FK          |
| description                |
| amount                     |
| category                   |
+----------------------------+
```

A trip can have multiple expenses, so the relationship is one-to-many.

The `planned_budget` field belongs to the Trip table because it represents a planned property of the trip itself. Actual expenses belong to the Expense table because they represent individual spending transactions.

This schema supports the application's central business calculation:

remaining_budget =
    planned_budget - total_expenses


SQLite was selected because the assignment explicitly requires SQLite and because it is appropriate for a small single-process application. It also avoids introducing an external database dependency before the project reaches the later containerization and deployment stage.

---

# 6. README.md

The README.md is saved as a separate file also within this project repository 

---

# 7. AI Usage

I acknowledge the use of ChatGPT for implementation guidance, architectural discussion, debugging, testing, and documentation. The AI suggestions were not treated as automatically correct. They were reviewed and verified through tests or manual application checks.

The prompts used included:

* Help set up the SQLite database and Trip model for the Study-Abroad-Trip-Planner
* Help implement CRUD operations and tests for trips
* Help establish the Expense domain separately from the Trip domain
* Help implement expense CRUD operations and testing.
* Help create an application service that combines trip and expense information.
* Help isolate trip tests from the application database.
* Help update the ADR documentation to explain project decisions and exclusions.
* Help create a README explaining the project and how to run it.
* Help convert the interactive application into a Flask application and integrate planned budget for comaprison

The output of these prompts was used to:

 * Set up the project domains
 * Establish CRUD operations
 * Implement testing and validation
 * Write documentation
