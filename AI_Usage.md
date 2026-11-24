# AI Usage Log

## 1. SQLite Setup

**Commit:** fe17fed
**Tool:** ChatGPT

**Prompt**

Help set up the SQLite database and Trip model for the Study-Abroad-Trip-Planner.

**Disposition**

Accepted

**What changed and why (if modified):** 

The suggested structure was adapted to the project's existing package organization.

**How this works (in my own words)** 

The Trip model represents a trip as an object with fields such sa name, destination, and dates. 
The database connection module creates the SQLite database and manages it. 

---

## 2. CRUD Operations

**Commit:** 64071cc
**Tool:** ChatGPT

**Prompt**

Help implement CRUD operations and tests for trips

**Disposition**

Modified

**What changed and why (if modified):** 

The approach was adapted to the project's service layer structure and the tests were modified to have more coverage.

**How this works (in my own words)** 

The trip service performs create, read, update, and delete operations by executing the SQL queries that are in the parameters against the SQLite. After that, it converts the database rows into Trip objects.

---

## 3. Expense Domain Design and Implementation

**Commit:** 33cd64f
**Tool:** ChatGPT

**Prompt**

Help establish the expense domain separately from the Trip domain

**Disposition**

Modified

**What changed and why (if modified):** 

Organized the expense domain into its own model and service modules. 

**How this works (in my own words)** 

The Expenses domain represents the actual spending that is done and reference a trip through the trip_id field. 
By keeping the model separate from the service, we prevent the Trip domain owning info that should be expense-specific. 

---

## 4. Expense CRUD Operations

**Commit:** 86e8200
**Tool:** ChatGPT

**Prompt**

Help implement expense CRUD operations and testing.

**Disposition**

Modified

**What changed and why (if modified):** 

The implementation was adjusted to match the project's validation rules and database structure.

**How this works (in my own words)** 

The Expense CRUD SQL operations through the expense service. 
We add additional testing to prevent invalid amounts and check for required fields that may be missing.

---

## 5. Trip and Expense Applications

**Commit:** 6e281da
**Tool:** ChatGPT

**Prompt**

Help create an application service that combines trip and expense information.

**Disposition**

Modified

**What changed and why (if modified):** 

The application service was kept separate from the domain services.

**How this works (in my own words)** 

The application layer calls both domain services and combines their results.
This allows the Trip and Expense domains to remain separately responsible for their own data.

---

## 6. Trip Test Isolation

**Commit:** 7929a36
**Tool:** ChatGPT

**Prompt**

Help isolate trip tests from the application database.

**Disposition**

Modified

**What changed and why (if modified):** 

Tests were changed to use a separate test database rather than modifying the real SQLite database.

**How this works (in my own words)** 

Each test uses an isolated database so that the test data does not accidentally change the application's real data.

---

## 6. ADR Documentation

**Commit:** e230987
**Tool:** ChatGPT

**Prompt**

Help update the ADR documentation to explain project decisions and exclusions.

**Disposition**

Modified

**What changed and why (if modified):** 

The ADRs were kept to exactly five entries as required by the assignment.

**How this works (in my own words)** 

ADRs are meant to record important decisions and the reasonings behind.
It allows whoever reviewing the project to understand its architecture.

---

## 7. README File

**Commit:** 0a943f0
**Tool:** ChatGPT

**Prompt**

Help create a README explaining the project and how to run it.

**Disposition**

Modified

**What changed and why (if modified):** 

The README was adapted to the project's actual commands, structure, and testing process.

**How this works (in my own words)** 

The README provides important setup instructions, explains the project's architecture, and documents how to run and test the application.

---

## 8. Flask API and Planned Budget

**Commit:** b0c5c81
**Tool:** ChatGPT

**Prompt**

Help convert the interactive application into a Flask application and integrate planned budget for comaprison

**Disposition**

Accepted

**What changed and why (if modified):** 

**How this works (in my own words)** 

Flask creates HTTP routes that call the application's servic layer. PORT is what lets the runtime choose the server port while 0.0.0.0 allows the application to accept connections from outside the local machine.
As for the plannet budget, a trip stores a planned budget (how much the user expects to spend), while expenses store the actual spending. The application layer subtracts the actual expenses from the planned budget to calculate the remaining budget. 

---

**## 9. SQL Server Database Separation and Service Communication**

**Commit:** 33db58c and 472c8ab
**Tool:** ChatGPT

**Prompt**

Help migrate the Trips and Expenses services from a shared SQLite database to separate SQL Server databases. Implement versioned migrations, preserve existing records, and update Expenses to validate trips through HTTP communication with Trips.

**Disposition**

Accepted

**What changed and why (if modified):**

Both services were migrated to independent SQL Server databases, TripsDB and ExpensesDB, with separate database credentials. Each service received its own database connection module, versioned migrations, migration runner, and legacy data import script. Existing record IDs and data were preserved. The Trips database also received a migration adding a nullable notes column.

The Expenses service now calls the Trips API to verify a trip exists before creating an expense. HTTP timeouts and error handling were added for missing trips and service outages. Dockerfiles were created with the dependencies needed for SQL Server connectivity.

**How this works (in my own words):**

Each service reads its DATABASE_URL environment variable to connect to its own SQL Server database using pyodbc. Migration files define schema changes, while the migration runner tracks applied versions in a schema_migrations table to prevent migrations from running more than once.

The import scripts transfer existing SQLite records while preserving their IDs. Since the services no longer share a database, expenses service cannot use a foreign key to verify trips. Instead, it sends an HTTP request to Trips before inserting an expense. If the trip doesn't exist or Trips is unavailable, Expenses returns an appropriate error rather than creating an invalid record.