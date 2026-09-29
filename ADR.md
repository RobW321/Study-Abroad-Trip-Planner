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
