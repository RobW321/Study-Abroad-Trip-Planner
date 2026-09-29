# Architecture Decision Records

## [1]. Use Flask and Python for the Backend

Date: 2026-09-29
Status: Decided

Context: The application needs a lightweight backend framework that can support two distinct feature domains while remaining simple enough to develop and deploy as a single-process monolith. The project also needs to remain easy to understand and explain during the comprehension check.

Decision: Use Python with Flask as the backend framework. Flask provides the routing and application structure needed for the project without introducing unnecessary framework complexity.

Alternatives considered: Django was considered because it provides more built-in functionality, but it was rejected because the application's scope does not require Django's larger framework and built-in components.

Consequences: The application will have a lightweight backend with explicit control over its routes and business logic. This reduces framework overhead but means some functionality must be implemented directly by the application.
