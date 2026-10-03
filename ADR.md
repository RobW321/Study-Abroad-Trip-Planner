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


**## [4]. Testing Approach**

Date: 2026-10-03

Status: Decided

Context: The project requires automated testing with a target of at least 70% code coverage. Testing time was prioritized toward the core business logic and data-access behavior of the two feature domains. These areas contain the application's primary functionality and are more important to verify than framework or presentation code.

Decision: Use pytest to test the trip and expense domains, database initialization, and trip-summary behavior. Tests prioritize CRUD operations, relationships between trips and expenses, and important edge cases such as retrieving or deleting a nonexistent trip. pytest-cov is used to measure coverage. The current test suite contains 20 tests and achieves 87% overall coverage.

Alternatives considered: Attempting to achieve 100% coverage across the entire application was considered, but rejected because coverage percentage alone does not guarantee meaningful tests. Prioritizing every Flask route equally was also rejected because the core domain and data logic provide greater value to test at this stage.

Consequences: The core application logic has strong automated test coverage and exceeds the required 70% target. Flask application routing in `app.py` remains thinner because the project prioritizes domain and data behavior over exhaustive framework-level testing. Additional route tests could be added if the application grows.


**## [5]. Deliberately Exclude User Authentication**

Date: 2026-10-03

Status: Decided

Context: A production trip-planning application would typically support
multiple users and require authentication and authorization. However, the
assignment focuses on modular feature domains, data modeling, automated
testing, and designing a monolithic application that could later be
decomposed into services. Authentication would introduce additional
infrastructure and security concerns that are outside the primary scope of
the project.

Decision: Do not implement user authentication or authorization. The
application will operate as a single-user demonstration application, with
trips and expenses managed without login or account management.

Alternatives considered: Implementing username/password authentication or
token-based authentication was considered, but rejected because it would
increase implementation complexity without materially improving the core
feature domains required by the assignment.

Consequences: The application has a smaller and more focused scope and avoids
introducing unnecessary authentication infrastructure. The tradeoff is that
the application is not designed for multiple users or production deployment
where user-specific data and access control would be required.