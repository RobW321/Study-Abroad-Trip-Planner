from expenses.model import Expense


def validate_expense(expense):
    if expense.amount < 0:
        raise ValueError("Expense amount cannot be negative")

    if not expense.description.strip():
        raise ValueError("Expense description cannot be empty")

    if not expense.category.strip():
        raise ValueError("Expense category cannot be empty")