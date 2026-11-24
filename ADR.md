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


**## [6]. Split the Application into Trips and Expenses Services**

Date: 2026-11-24

Status: Decided

Context: The original application operated as a single Flask application with trip-planning and expense-tracking functionality. Assignment 2 required the application to be separated into independently deployable services while preserving the existing domain responsibilities. The main architectural question was where to establish the service boundary and how the two domains would communicate without sharing application code or directly accessing each other's databases.

Decision: Split the application into two backend services: a Trips service and an Expenses service. The Trips service owns trip-related operations and data, while the Expenses service owns expense-related operations and data. The service boundary remains between the two domains, consistent with the original separation established in ADR-2. The existing domain seam held so there was no need to move it. Communication across the boundary also occurs through HTTP APIs. For example, when an expense is created, the Expenses service sends an HTTP request to the Trips service to verify that the referenced trip exists. The Expenses service does not directly access the Trips database. The Trips service does not directly access the Expenses database.

Alternatives considered: Keeping both domains inside one Flask application was considered, but this would not provide independent deployment or runtime isolation. Another option was allowing both services to share a database, but this would create unnecessary coupling and weaken the separation between the domains. A message broker was also considered as a possible communication mechanism, but direct HTTP communication was simpler and sufficient for the synchronous validation required by the application.

Consequences: Each service can be developed, tested, deployed, and operated independently. The service boundary introduces network-related failure possibilities, so outbound HTTP requests require timeouts and error handling. If the Trips service is unavailable, the Expenses service returns an appropriate error rather than creating an expense without validating its trip. This preserves the domain responsibilities while reducing direct coupling between the services.


**## [7]. Separate Databases and Introduce Versioned Migrations**

Date: 2026-11-24

Status: Decided

Context: The original application stored both trips and expenses in a single SQLite database. Splitting the application into independent services meant that each service needed ownership of its own persistent data. This required moving the existing data into separate databases while preserving existing records and maintaining the relationship between expenses and trips across the service boundary.

Decision: Give the Trips service exclusive ownership of a TripsDB database and the Expenses service exclusive ownership of an ExpensesDB database. Both databases use SQL Server, with separate database logins and credentials. Existing records are migrated from the original SQLite database using dedicated import scripts that preserve record IDs and existing values.

Each service manages its schema through versioned SQL migration files. A schema_migrations table records which migrations have already been applied, preventing migrations from being repeatedly executed during application startup. The Trips database includes a second migration that adds a nullable notes column to the existing trips table without dropping or recreating existing records. The database split removes the original database-level foreign key relationship between expenses and trips. Instead, the Expenses service maintains the trip_id reference and validates that the referenced trip exists by calling the Trips service over HTTP before creating an expense. The Expenses database does not contain a foreign key referencing the Trips database.

For recovery from a failed migration, the affected service should be stopped and the database backed up or snapshotted before recovery work begins. If a migration fails, its transaction should be rolled back and its version should not be recorded as successfully applied. If an already-applied migration causes a problem, restore the affected database from a backup taken before that migration, correct the issue, and apply a new or corrected migration. After recovery, verify the schema, migration history, and existing records before restarting the service.

Alternatives considered: Keeping a shared database would have preserved the original foreign key relationship, but it would prevent each service from having independent database ownership. Replacing the original tables instead of migrating them was rejected because it could result in data loss. Application startup schema creation was also rejected in favor of explicit, versioned migrations because migrations provide a controlled and traceable way to evolve the database.

Consequences: Each service now controls its own database, credentials, and schema changes. This improves service independence and prevents one service from directly accessing the other service's data. However, referential integrity between trips and expenses is no longer enforced by a database foreign key. The HTTP validation performed by the Expenses service compensates for this loss when creating expenses, although it cannot provide the same guarantees as a cross-domain database transaction. Versioned migrations, preserved record IDs, and database backups provide a repeatable approach to schema changes and recovery.