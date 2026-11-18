
const TRIPS_API = window.APP_CONFIG.TRIPS_API_URL;
const EXPENSES_API = window.APP_CONFIG.EXPENSES_API_URL;

let selectedTripId = null;


function showMessage(message) {
    document.getElementById("message").textContent = message;
}



async function loadTrips() {
    console.log("loadTrips() started");

    try {
        const response = await fetch(`${TRIPS_API}/trips`);

        if (!response.ok) {
            throw new Error(`Trips service error: ${response.status}`);
        }

        const data = await response.json();

        console.log("Trips received:", data.trips);

        const tripList = document.getElementById("trip-list");
        tripList.innerHTML = "";

        if (data.trips.length === 0) {
            tripList.textContent = "No trips found.";
            return;
        }

        data.trips.forEach(trip => {
            const item = document.createElement("div");
            item.className = "trip-item";

            const title = document.createElement("h3");
            title.textContent = trip.name;

            const destination = document.createElement("p");
            destination.textContent = trip.destination;

            const button = document.createElement("button");
            button.textContent = "View Details";
            button.type = "button";

            button.onclick = function () {
                loadTripDetails(trip.id);
            };

            item.append(title, destination, button);
            tripList.appendChild(item);
        });

        console.log("Trip buttons created successfully.");

    } catch (error) {
        console.error("Error loading trips:", error);
        showMessage(error.message);
    }
}




async function loadTripDetails(tripId) {
    console.log("View Details clicked. Trip ID:", tripId);

    try {
        const [tripResponse, expenseResponse] = await Promise.all([
            fetch(`${TRIPS_API}/trips/${tripId}`),
            fetch(`${EXPENSES_API}/trips/${tripId}/expenses`)
        ]);

        console.log("Trips response:", tripResponse.status);
        console.log("Expenses response:", expenseResponse.status);

        if (!tripResponse.ok) {
            throw new Error(`Trips service error: ${tripResponse.status}`);
        }

        if (!expenseResponse.ok) {
            throw new Error(`Expenses service error: ${expenseResponse.status}`);
        }

        const tripData = await tripResponse.json();
        const expenseData = await expenseResponse.json();

        console.log("Trip data:", tripData);
        console.log("Expense data:", expenseData);

        const trip = tripData.trip;
        const expenses = expenseData.expenses;

        selectedTripId = tripId;

        // Show the trip details section
        document.getElementById("trip-details").hidden = false;

        // Display trip information
        document.getElementById("trip-information").textContent =
            `${trip.destination} | ${trip.start_date} to ${trip.end_date}`;

        // Display expenses
        const expenseList = document.getElementById("expense-list");
        expenseList.innerHTML = "";

        if (expenses.length === 0) {
            expenseList.textContent = "No expenses recorded yet.";
        } else {
            expenses.forEach(expense => {
                const item = document.createElement("div");
                item.className = "expense-item";

                item.textContent =
                    `${expense.description} — ${Number(expense.amount).toFixed(2)} (${expense.category})`;

                expenseList.appendChild(item);
            });
        }

        // Calculate budget summary
        const totalExpenses = expenses.reduce(
            (total, expense) => total + Number(expense.amount),
            0
        );

        const remainingBudget = Number(trip.planned_budget) - totalExpenses;

        document.getElementById("budget-summary").textContent =
            `Planned budget: ${Number(trip.planned_budget).toFixed(2)} | ` +
            `Total expenses: ${totalExpenses.toFixed(2)} | ` +
            `Remaining budget: ${remainingBudget.toFixed(2)}`;

        console.log("Trip details rendered successfully.");

        showMessage("");

    } catch (error) {
        console.error("Error loading trip details:", error);
        showMessage(error.message);
    }
}



document.getElementById("trip-form").addEventListener("submit", async event => {
    event.preventDefault();

    const formData = new FormData(event.target);

    const trip = Object.fromEntries(formData.entries());
    trip.planned_budget = Number(trip.planned_budget);

    try {
        const response = await fetch(`${TRIPS_API}/trips`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(trip)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to create trip");
        }

        event.target.reset();
        showMessage("Trip created successfully.");
        await loadTrips();

    } catch (error) {
        showMessage(error.message);
    }
});


document.getElementById("expense-form").addEventListener("submit", async event => {
    event.preventDefault();

    if (selectedTripId === null) {
        showMessage("Select a trip first.");
        return;
    }

    const formData = new FormData(event.target);

    const expense = Object.fromEntries(formData.entries());
    expense.trip_id = selectedTripId;
    expense.amount = Number(expense.amount);

    try {
        const response = await fetch(`${EXPENSES_API}/expenses`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(expense)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to create expense");
        }

        event.target.reset();
        showMessage("Expense added successfully.");

        await loadTripDetails(selectedTripId);

    } catch (error) {
        showMessage(error.message);
    }
});


loadTrips();
