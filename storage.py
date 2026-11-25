"""
Storage Module (Ashish - CSV Data Storage)
Handles reading, writing, updating, and deleting records from CSV files.
"""

import csv
import os

EXPENSES_FILE = "expenses.csv"
BUDGET_FILE = "budget.csv"

EXPENSE_FIELDNAMES = ["id", "date", "category", "description", "amount"]


def initialize_storage():
    """Ensure data files exist with appropriate headers."""
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=EXPENSE_FIELDNAMES)
            writer.writeheader()

    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["monthly_budget", "15000.0"])


def load_expenses():
    """Read all expenses from the CSV file."""
    initialize_storage()
    records = []
    with open(EXPENSES_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                records.append({
                    "id": int(row["id"]),
                    "date": row["date"].strip(),
                    "category": row["category"].strip(),
                    "description": row["description"].strip(),
                    "amount": float(row["amount"])
                })
            except (ValueError, KeyError):
                continue
    return records


def save_expenses(expenses):
    """Write the full list of expense records to the CSV file."""
    with open(EXPENSES_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=EXPENSE_FIELDNAMES)
        writer.writeheader()
        for exp in expenses:
            writer.writerow({
                "id": exp["id"],
                "date": exp["date"],
                "category": exp["category"],
                "description": exp["description"],
                "amount": f"{exp['amount']:.2f}"
            })


def load_budget():
    """
    Read the monthly budget and any category limits from the budget CSV.
    Returns:
        tuple: (monthly_budget: float, category_budgets: dict)
    """
    initialize_storage()
    monthly_budget = 15000.0
    category_budgets = {}

    with open(BUDGET_FILE, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 2:
                continue
            key = row[0].strip()
            val = row[1].strip()
            try:
                num = float(val)
                if key.lower() == "monthly_budget":
                    monthly_budget = num
                else:
                    category_budgets[key] = num
            except ValueError:
                continue

    return monthly_budget, category_budgets


def save_budget(monthly_budget, category_budgets=None):
    """Save the monthly budget and optional category budgets to the CSV file."""
    if category_budgets is None:
        category_budgets = {}

    with open(BUDGET_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["monthly_budget", f"{monthly_budget:.2f}"])
        for cat, limit in category_budgets.items():
            writer.writerow([cat, f"{limit:.2f}"])
