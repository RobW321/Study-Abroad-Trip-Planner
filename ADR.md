# Architecture Decision Records

## [1]. Use Flask and Python for the Backend

Date: 2026-09-29
Status: Decided

Context: The application needs a lightweight backend framework that can support two distinct feature domains while remaining simple enough to develop and deploy as a single-process monolith. The project also needs to remain easy to understand and explain during the comprehension check.

Decision: Use Python with Flask as the backend framework. Flask provides the routing and application structure needed for the project without introducing unnecessary framework complexity.

Alternatives considered: Django was considered because it provides more built-in functionality, but it was rejected because the application's scope does not require Django's larger framework and built-in components.

Consequences: The application will have a lightweight backend with explicit control over its routes and business logic. This reduces framework overhead but means some functionality must be implemented directly by the application.


## [2]. Separate Trip Planning and Expense Tracking into Independent Domains

Date: 2026-09-29
Status: Decided

Context: The application has two distinct responsibilities: planning trips and activities before or during travel, and recording actual expenses during a trip. These responsibilities use different data and business logic and should remain loosely coupled so either domain could later be extracted into its own service.

Decision: Organize the backend into separate Trip Planning and Expense Tracking domains, with each domain owning its own routes, business logic, and data access. A higher-level dashboard can combine information from both domains without making either domain directly dependent on the other.

Alternatives considered: A single trip-management module containing both planning and expense functionality was considered, but it was rejected because it would make the two responsibilities more tightly coupled and make a future transition to separate services more difficult.

Consequences: The project will have slightly more structure than a single-module application, but the separation makes responsibilities clearer and supports the assignment's future microservice decomposition.


## [3]. Associate Expenses with Trips

### Status
Accepted

### Context

The StudyTrip Planner needs to track expenses for individual trips.
A user may have multiple trips and each trip may contain many expenses.

We need a way to associate each expense with the trip it belongs to while
keeping the trip and expense domains separately organized.

### Decision

Each expense will store a `trip_id` that references the corresponding trip.

The database will enforce this relationship through a foreign key.

The expense model will therefore contain `trip_id`, while expense-specific
logic will remain inside the expense domain.

### Consequences

This allows:

- Multiple expenses to belong to one trip.
- Expenses to be retrieved for a specific trip.
- Trip and expense functionality to remain separated.
- The database to maintain the relationship between trips and expenses.

The tradeoff is that expense operations need to know the associated trip ID,
and database queries involving both domains may require joins or multiple
queries.


**## [4]. Use a Separate Database for Automated Tests**

Date: 2026-10-03

Status: Decided

Context: The application uses SQLite for persistent data. Automated tests need to create, update, and delete trips without modifying the application's real `studytrip.db` database. Using the production database during tests could cause test data to persist between runs and make test results dependent on previous test execution.

Decision: Automated tests will use a separate `test_studytrip.db` database. The test setup will configure the database connection to use this test database before each test, and the test database will be deleted after each test completes.

Alternatives considered: Using the application's `studytrip.db` directly was considered, but it was rejected because test data could interfere with real application data and make tests less isolated. An in-memory SQLite database was also considered, but a separate test database keeps the setup closer to the application's existing SQLite configuration.

Consequences: Tests are isolated from production data and can be run repeatedly without accumulating test records. The test suite requires additional setup and cleanup, but this improves test reliability and makes failures easier to reproduce.