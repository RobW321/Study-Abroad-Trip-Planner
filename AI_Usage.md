# AI Usage Log

This document records meaningful uses of AI assistance during development of the Study-Abroad Trip Planner. AI was used as a development aid; implementation decisions, code execution, testing, and verification were performed by the developer.

---

## 1. Project Scope and Architecture

**Date:** 2026-09-XX
**Purpose:** Define the application scope and identify two genuinely distinct backend feature domains.

**AI Contribution:**

* Helped evaluate the proposed study-abroad trip planner against the assignment requirement for two distinct backend feature domains.
* Suggested separating the application into:

  * Trip Planning
  * Expense Tracking
* Helped establish a meaningful reason for the domains to interact through trip spending summaries.

**Developer Action / Verification:**

* Reviewed the proposed architecture.
* Chose the final domain boundaries and application purpose.
* Implemented the architecture independently in the project.

**Result:** Established the two-domain project scope.

---

## 2. Flask and SQLite Setup

**Date:** 2026-09-XX
**Purpose:** Establish the initial backend structure and persistence layer.

**AI Contribution:**

* Provided guidance on structuring the Flask/Python application.
* Discussed using SQLite for persistence.
* Suggested separating database connection logic from domain services.

**Developer Action / Verification:**

* Created the project structure.
* Implemented the database connection and initialization logic.
* Created the initial SQLite schema.
* Ran the application and verified that the database initialized correctly.

**Result:** Established the initial backend and SQLite persistence layer.

---

## 3. Trip Domain Implementation

**Date:** 2026-09-XX
**Purpose:** Implement the Trip Planning domain.

**AI Contribution:**

* Assisted with designing the `Trip` model.
* Provided guidance for implementing CRUD service operations.
* Helped reason through how the service layer should interact with SQLite.

**Developer Action / Verification:**

* Implemented the Trip model.
* Implemented create, read, update, and delete operations.
* Tested the operations using pytest.
* Manually verified the application behavior.

**Result:** Completed the Trip Planning domain.

---

## 4. Expense Domain Design and Implementation

**Date:** 2026-09-XX
**Purpose:** Add a second backend domain with a meaningful relationship to trips.

**AI Contribution:**

* Helped determine how Expense Tracking could function as a distinct feature domain.
* Suggested associating each expense with a trip using `trip_id`.
* Helped reason about validation and the requirement that an expense reference an existing trip.

**Developer Action / Verification:**

* Created the Expense model.
* Implemented expense CRUD operations.
* Added expense validation.
* Implemented the trip relationship using `trip_id`.
* Tested the expense functionality.

**Result:** Completed the Expense Tracking domain while maintaining separation from Trip Planning.

---

## 5. Application-Layer Integration

**Date:** 2026-09-XX
**Purpose:** Give the two domains a meaningful cross-domain purpose.

**AI Contribution:**

* Helped design an application service that combines trip information with its associated expenses.
* Suggested calculating total spending in the application layer rather than coupling the two domain services.
* Helped define the trip summary workflow.

**Developer Action / Verification:**

* Implemented `application/trip_summary.py`.
* Connected the Trip and Expense services through the application layer.
* Wrote tests for trip summaries and expense totals.
* Verified that expenses were correctly associated with the selected trip.

**Result:** Created meaningful cross-domain functionality rather than two unrelated CRUD modules.

---

## 6. Testing Strategy

**Date:** 2026-09-XX
**Purpose:** Establish a testing strategy that prioritizes the core backend behavior.

**AI Contribution:**

* Recommended prioritizing tests around:

  * Trip Planning
  * Expense Tracking
  * Database behavior
  * Domain relationships
  * Application-layer functionality
* Recommended avoiding artificial efforts to maximize coverage of CLI input/output code.

**Developer Action / Verification:**

* Implemented pytest tests across the project.
* Ran the complete test suite with coverage.
* Reviewed uncovered code and determined that the CLI layer did not require exhaustive testing.

**Result:** Reached 20 passing tests and 87% overall code coverage.

---

## 7. Test Isolation

**Date:** 2026-09-XX
**Purpose:** Prevent tests from modifying the production SQLite database.

**AI Contribution:**

* Identified the importance of isolating tests from the application's `studytrip.db`.
* Suggested using a separate test database during trip tests.
* Helped design setup and teardown behavior for the test database.

**Developer Action / Verification:**

* Updated test setup to use `test_studytrip.db`.
* Added teardown logic to remove the test database after each test.
* Ran the test suite and verified that tests passed without relying on production data.

**Result:** Improved test isolation and prevented test data from polluting the application database.

---

## 8. Edge-Case Testing

**Date:** 2026-09-XX
**Purpose:** Increase confidence in error handling beyond normal CRUD operations.

**AI Contribution:**

* Suggested testing nonexistent trips and other invalid domain scenarios.
* Helped identify cases that should return `None` or raise `ValueError`.

**Developer Action / Verification:**

* Added edge-case tests for nonexistent trip operations and domain validation.
* Executed the tests and verified the expected behavior.

**Result:** Increased confidence in error handling and contributed to the 87% overall coverage result.

---

## 9. Architecture Decision Record

**Date:** 2026-09-XX
**Purpose:** Document the project's major architectural decisions.

**AI Contribution:**

* Helped organize the required ADR entries around:

  1. Backend language/framework choice
  2. Independent feature-domain boundaries
  3. SQLite schema and data-model decisions
  4. Testing approach
  5. A deliberately excluded feature
* Helped clarify how the architecture supports potential future service extraction.

**Developer Action / Verification:**

* Reviewed each architectural decision.
* Made the final decisions about Flask, domain separation, SQLite relationships, testing priorities, and scope exclusions.
* Wrote and finalized `ADR.md`.

**Result:** Documented the project's major architectural decisions and deliberate scope limitations.

---

## 10. Final Integration Validation

**Date:** 2026-10-04
**Purpose:** Validate the complete application workflow before submission.

**AI Contribution:**

* Reviewed the final application flow.

* Recommended validating the complete workflow:

  `Trip → Expenses → Summary → Dashboard`

* Recommended testing both valid and invalid user input.

**Developer Action / Verification:**

* Ran `python app.py`.
* Verified that existing trips were displayed.
* Selected trips and verified their associated expenses.
* Verified that total spending was calculated correctly.
* Tested an invalid trip ID.
* Tested invalid non-numeric input.

**Result:** Confirmed that the integrated application workflow works as intended.

---

## 11. Repository Cleanup

**Date:** 2026-10-04
**Purpose:** Prepare the Git repository for final submission.

**AI Contribution:**

* Helped identify generated coverage output that should not be committed.
* Recommended adding `.coverage` to `.gitignore`.
* Identified the stale Git upstream configuration.

**Developer Action / Verification:**

* Added `.coverage` to `.gitignore`.
* Verified that `studytrip.db` was already ignored.
* Verified that generated files such as `.coverage`, `.pyc`, `venv`, and `.pytest_cache` were not tracked.
* Removed the stale upstream configuration.
* Verified that the working tree was clean.

**Result:** Prepared a clean repository containing only the relevant project files.

---

## 12. Project Documentation

**Date:** 2026-10-04
**Purpose:** Document the project for final submission.

**AI Contribution:**

* Assisted in drafting a concise `README.md`.
* Helped organize documentation covering:

  * Project purpose
  * Two-domain architecture
  * Application-layer integration
  * SQLite schema
  * Project structure
  * Running the application
  * Running tests
  * Example workflow
  * Architectural decisions

**Developer Action / Verification:**

* Reviewed the generated documentation.
* Verified that the documented architecture matched the actual implementation.
* Added and committed `README.md`.

**Result:** Added documentation explaining how to run, test, and understand the project.

---

## Final Verification

The final project was manually and automatically verified after development.

* **20 automated tests passing**
* **87% overall code coverage**
* Trip Planning domain implemented and tested
* Expense Tracking domain implemented and tested
* Application layer integrates the two domains
* SQLite persistence implemented
* README documentation added
* ADR documentation completed
* Generated development artifacts excluded from Git
* Working tree clean
