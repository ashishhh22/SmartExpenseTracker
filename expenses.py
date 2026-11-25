"""
Expense Management Module (Jiya - Expense Management)
Handles adding, editing, deleting, and validating expense records using the Expense OOP Model.
"""

from datetime import datetime
import storage
from models import Expense, RecurringExpense

DEFAULT_CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Entertainment",
    "Education",
    "Bills",
    "Others"
]


def validate_date(date_str):
    """
    Validate and normalize date string.
    Accepts formats: DD-Mon-YYYY (e.g. 01-Oct-2026), YYYY-MM-DD, DD-MM-YYYY, DD/MM/YYYY.
    Returns normalized string 'DD-Mon-YYYY' or None if invalid.
    """
    if not date_str:
        return None
    date_str = str(date_str).strip()
    formats = [
        "%d-%b-%Y",  # 01-Oct-2026
        "%Y-%m-%d",  # 2026-10-01
        "%d-%m-%Y",  # 01-10-2026
        "%d/%m/%Y",  # 01/10/2026
    ]
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            return parsed.strftime("%d-%b-%Y")
        except ValueError:
            continue
    return None


def validate_amount(amount_input):
    """Validate that amount is a positive number."""
    try:
        val = float(amount_input)
        if val <= 0:
            return None
        return round(val, 2)
    except (ValueError, TypeError):
        return None


def get_all_expenses():
    """Retrieve all expenses as raw dictionaries."""
    return storage.load_expenses()


def get_all_expense_objects():
    """
    Retrieve all expenses as instantiated Expense domain objects (Activity 6).
    Demonstrates Encapsulation and Object Modeling.
    """
    raw_list = storage.load_expenses()
    return [Expense.from_dict(d) for d in raw_list]


def add_expense(date_str, category, description, amount):
    """
    Add a new expense record using the Expense class for validation and encapsulation.
    Returns:
        tuple: (success: bool, message: str, record: dict)
    """
    expenses = storage.load_expenses()
    next_id = max([e["id"] for e in expenses], default=0) + 1

    try:
        # Create domain object which validates inputs via setters
        exp_obj = Expense(
            expense_id=next_id,
            date_str=date_str,
            category=category,
            description=description,
            amount=amount
        )
    except ValueError as err:
        return False, str(err), None

    record = exp_obj.to_dict()
    expenses.append(record)
    storage.save_expenses(expenses)
    return True, "Expense added successfully.", record


def edit_expense(expense_id, date_str=None, category=None, description=None, amount=None):
    """
    Edit an existing expense record by ID using domain model mutation.
    Returns:
        tuple: (success: bool, message: str)
    """
    expenses = storage.load_expenses()
    target_idx = None
    for idx, e in enumerate(expenses):
        if e["id"] == expense_id:
            target_idx = idx
            break

    if target_idx is None:
        return False, f"Expense with ID #{expense_id} not found."

    current_data = expenses[target_idx]
    try:
        exp_obj = Expense.from_dict(current_data)
        if date_str is not None and date_str.strip():
            exp_obj.date = date_str
        if category is not None and category.strip():
            exp_obj.category = category
        if description is not None and description.strip():
            exp_obj.description = description
        if amount is not None and str(amount).strip():
            exp_obj.amount = amount
    except ValueError as err:
        return False, str(err)

    expenses[target_idx] = exp_obj.to_dict()
    storage.save_expenses(expenses)
    return True, f"Expense #{expense_id} updated successfully."


def delete_expense(expense_id):
    """
    Delete an expense record by ID.
    Returns:
        tuple: (success: bool, message: str)
    """
    expenses = storage.load_expenses()
    initial_count = len(expenses)
    filtered = [e for e in expenses if e["id"] != expense_id]

    if len(filtered) == initial_count:
        return False, f"Expense with ID #{expense_id} not found."

    storage.save_expenses(filtered)
    return True, f"Expense #{expense_id} deleted successfully."
