# Architecture Decision Records

**## [1]. Use Flask and Python for the Backend**

Date: 2026-09-29

Status: Decided

Context: The application needs a lightweight backend framework that can support two distinct feature domains while remaining simple enough to develop and deploy as a single-process monolith. The project also needs to remain easy to understand and explain during the comprehension check.

Decision: Use Python with Flask as the backend framework. Flask provides the routing and application structure needed for the project without introducing unnecessary framework complexity.

Alternatives considered: Django was considered because it provides more built-in functionality, but it was rejected because the application's scope does not require Django's larger framework and built-in components.

Consequences: The application will have a lightweight backend with explicit control over its routes and business logic. This reduces framework overhead but means some functionality must be implemented directly by the application.


**## [2]. Separate the Application into Trip Planning and Expense Tracking Domains**

Date: 2026-09-30

Status: Decided

Context: The assignment requires two genuinely distinct backend feature domains that have separate responsibilities and data and could potentially be extracted into independent services in the future. The domains should therefore be separated without creating unnecessary coupling between them.

Decision: Separate the application into a Trip Planning domain and an Expense Tracking domain. The Trip Planning domain is responsible for trip information and planned budgets, while the Expense Tracking domain is responsible for actual expenses. A separate application layer coordinates information from both domains when a combined trip summary is needed.

Alternatives considered: A single service containing both trip and expense logic was considered because it would be simpler initially, but it was rejected because it would make the two feature areas more tightly coupled and would not demonstrate the modular domain structure required by the assignment.

Consequences: Each domain has its own model and service layer and is responsible for its own data and business logic. The application layer can combine the domains without moving expense-specific logic into the Trip domain or trip-specific logic into the Expense domain. This provides a clearer path toward future microservice extraction.


**## [3]. Use SQLite with Separate Trip and Expense Tables**

Date: 2026-10-2

Status: Decided

Context: The application needs persistent storage for both backend domains while remaining a simple single-process monolith. The assignment requires SQLite and does not permit an external managed database for this stage of the project.

Decision: Use SQLite as the application's database with separate `trips` and `expenses` tables. The `trips` table stores trip information and `planned_budget`, while the `expenses` table stores individual expenses. Each expense contains a `trip_id` foreign key referencing the trip to which it belongs.

Alternatives considered: A separate database for each domain was considered because it could more closely resemble a future microservice architecture, but it was rejected because the assignment specifically requires SQLite and the application is currently a single monolith. A single combined table was also rejected because trip information and individual expenses represent different types of data and responsibilities.

Consequences: One trip can have many expenses through the `trip_id` relationship. The two domains remain logically separated even though they currently share one SQLite database. The application layer can use both tables to calculate actual spending and compare it with a trip's planned budget.


**## [4]. Use Pytest and Pytest-Cov for Automated Testing**

Date: 2026-10-03

Status: Decided

Context: The application needs automated tests for the core business logic of both backend domains and must achieve at least 70% code coverage. The most important areas to verify are database operations, domain behavior, validation, edge cases, and the application-layer budget calculations.

Decision: Use pytest for automated testing and pytest-cov for measuring code coverage. Testing will prioritize Trip CRUD operations, Expense CRUD operations, validation, database behavior, nonexistent-record cases, trip summaries, and planned-budget calculations.

Alternatives considered: Testing only the Flask routes was rejected because the majority of the application's business logic exists in the domain services and application layer. Testing every line of framework glue code was also rejected because it would provide less value than testing the core business behavior.

Consequences: The project has a focused automated test suite covering the most important business logic. The final test suite contains 21 passing tests and achieves 96% coverage, exceeding the assignment's 70% requirement. The Flask routing layer remains thinner and is tested less extensively because it primarily connects HTTP requests to already-tested application logic.


**## [5]. Deliberately Exclude Authentication and Authorization**

Date: 2026-10-03

Status: Decided

Context: A production trip-planning application could require user accounts, authentication, and authorization. However, the primary purpose of this assignment is to demonstrate backend domain separation, persistence, testing, version control, and preparation for future DevOps work.

Decision: Do not implement authentication or authorization in this version of the application. The application will operate as a simple single-user demonstration.

Alternatives considered: Implementing a user account system with authentication and authorization was considered, but it was rejected because it would introduce additional database structures, security concerns, and application complexity that are outside the primary scope of the assignment.

Consequences: The application remains small and focused on its two required backend domains. This reduces implementation and security complexity while leaving authentication as a potential feature for a future version when the application is expanded or split into independently deployed services.
