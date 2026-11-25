"""
Expense & Budget Analyzer
Main Application (Shreya - Integration, Flow & UI)

Enhanced for Milestone 2 Incorporating:
- Activity 3: Functional Decomposition
- Activity 4: Card Sorting & Algorithmic Process
- Activity 5: Decision Tree Controls & Anomaly Detection
- Activity 6: Object Modeling (Classes, Inheritance, Polymorphism)
- Activity 7: Visual Data Interpretation & Insights
"""

import sys
from datetime import datetime
import storage
import expenses
import analysis
from models import RecurringExpense


def print_banner():
    print("=" * 70)
    print("        EXPENSE & BUDGET ANALYZER - MILESTONE 2")
    print("      Personal Finance Management & Spending Insights System")
    print("=" * 70)


def print_menu():
    print("\n" + "-" * 50)
    print("                  MAIN MENU")
    print("-" * 50)
    print(" [1] View All Expenses (Tabular)")
    print(" [2] Add New Expense")
    print(" [3] Edit an Expense")
    print(" [4] Delete an Expense")
    print(" [5] View / Set Monthly Budget")
    print(" [6] Visual Spending Analysis & ASCII Chart  (Activity 7)")
    print(" [7] Decision Tree Alerts & Anomaly Insights (Activity 5)")
    print(" [8] OOP Domain Model Demonstration           (Activity 6)")
    print(" [9] Milestone Executive Summary")
    print(" [10] Reset with Milestone Sample Data")
    print(" [0] Exit")
    print("-" * 50)


def view_all_expenses():
    records = expenses.get_all_expenses()
    print("\n" + "=" * 80)
    print("                             RECORDED EXPENSES")
    print("=" * 80)
    if not records:
        print("  No expense records found. Add one from the main menu!")
        print("=" * 80)
        return

    print(f" {'ID':<4} | {'Date':<12} | {'Category':<15} | {'Description':<22} | {'Amount (INR)':>12}")
    print("-" * 80)
    for exp in records:
        print(f" #{exp['id']:<3} | {exp['date']:<12} | {exp['category']:<15} | {exp['description']:<22} | ₹{exp['amount']:>10,.2f}")
    print("-" * 80)
    total = sum(e["amount"] for e in records)
    print(f"  TOTAL EXPENSES: {len(records)} record(s) | Sum: ₹{total:,.2f}")
    print("=" * 80)


def add_expense_flow():
    print("\n--- Add New Expense ---")

    # Date
    today_str = datetime.now().strftime("%d-%b-%Y")
    date_input = input(f"Enter Date (DD-Mon-YYYY or YYYY-MM-DD) [Press Enter for today: {today_str}]: ").strip()
    if not date_input:
        date_input = today_str

    # Category selection
    print("\nSelect Category:")
    for i, cat in enumerate(expenses.DEFAULT_CATEGORIES, 1):
        print(f"  [{i}] {cat}")
    print("  [0] Custom Category")

    cat_choice = input(f"Choose category (1-{len(expenses.DEFAULT_CATEGORIES)}): ").strip()
    if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(expenses.DEFAULT_CATEGORIES):
        category = expenses.DEFAULT_CATEGORIES[int(cat_choice) - 1]
    elif cat_choice == "0":
        category = input("Enter custom category name: ").strip()
        if not category:
            category = "Others"
    else:
        category = "Others"

    # Description
    description = input("Enter Short Description (e.g. Lunch, Metro, Books): ").strip()
    if not description:
        description = "General Expense"

    # Amount
    amount_input = input("Enter Amount in ₹ (e.g. 250): ").strip()

    success, msg, record = expenses.add_expense(date_input, category, description, amount_input)
    if success:
        print(f"\n[SUCCESS] {msg}")
        print(f"Record added: #{record['id']} | {record['date']} | {record['category']} | {record['description']} | ₹{record['amount']:,.2f}")
    else:
        print(f"\n[ERROR] {msg}")


def edit_expense_flow():
    view_all_expenses()
    records = expenses.get_all_expenses()
    if not records:
        return

    id_input = input("\nEnter the ID of the expense to edit (or 0 to cancel): ").strip()
    if not id_input.isdigit() or int(id_input) == 0:
        return

    exp_id = int(id_input)
    match = next((e for e in records if e["id"] == exp_id), None)
    if not match:
        print(f"[ERROR] Expense ID #{exp_id} does not exist.")
        return

    print(f"\nEditing Expense #{exp_id} (Press Enter to keep current value)")
    print(f"Current Date: {match['date']}")
    new_date = input("New Date (or Enter to keep): ").strip()

    print(f"Current Category: {match['category']}")
    new_cat = input("New Category (or Enter to keep): ").strip()

    print(f"Current Description: {match['description']}")
    new_desc = input("New Description (or Enter to keep): ").strip()

    print(f"Current Amount: ₹{match['amount']:,.2f}")
    new_amount = input("New Amount (or Enter to keep): ").strip()

    success, msg = expenses.edit_expense(
        exp_id,
        date_str=new_date if new_date else None,
        category=new_cat if new_cat else None,
        description=new_desc if new_desc else None,
        amount=new_amount if new_amount else None
    )
    if success:
        print(f"\n[SUCCESS] {msg}")
    else:
        print(f"\n[ERROR] {msg}")


def delete_expense_flow():
    view_all_expenses()
    records = expenses.get_all_expenses()
    if not records:
        return

    id_input = input("\nEnter the ID of the expense to delete (or 0 to cancel): ").strip()
    if not id_input.isdigit() or int(id_input) == 0:
        return

    exp_id = int(id_input)
    confirm = input(f"Are you sure you want to delete expense #{exp_id}? (y/N): ").strip().lower()
    if confirm == "y":
        success, msg = expenses.delete_expense(exp_id)
        if success:
            print(f"\n[SUCCESS] {msg}")
        else:
            print(f"\n[ERROR] {msg}")
    else:
        print("Deletion canceled.")


def budget_flow():
    monthly_budget, _ = storage.load_budget()
    print("\n" + "=" * 50)
    print("               BUDGET MANAGEMENT")
    print("=" * 50)
    print(f" Current Monthly Budget: ₹{monthly_budget:,.2f}")
    print("-" * 50)
    choice = input("Do you want to update the monthly budget? (y/N): ").strip().lower()
    if choice == "y":
        new_b = input("Enter new monthly budget in ₹: ").strip()
        try:
            val = float(new_b)
            if val <= 0:
                print("[ERROR] Budget must be greater than 0.")
            else:
                storage.save_budget(val)
                print(f"[SUCCESS] Monthly budget updated to ₹{val:,.2f}")
        except ValueError:
            print("[ERROR] Please enter a valid numerical amount.")


def visual_spending_analysis_flow():
    """Activity 7: Data Interpretation & Visualization Flow."""
    records = expenses.get_all_expenses()
    monthly_budget, _ = storage.load_budget()
    summary = analysis.calculate_budget_summary(monthly_budget, records)

    print("\n" + "=" * 70)
    print("       SPENDING ANALYSIS & DATA VISUALIZATION (ACTIVITY 7)")
    print("=" * 70)
    print(f" Monthly Budget:           ₹{summary['monthly_budget']:>12,.2f}")
    print(f" Total Expenses:           ₹{summary['total_expenses']:>12,.2f}")
    print(f" Remaining Budget:         ₹{summary['remaining_budget']:>12,.2f}")
    print(f" Budget Used:              {summary['budget_used_pct']:>11.1f}%")
    print(f" Health Badge:             {summary['badge']}")
    print("-" * 70)

    # ASCII Chart
    print("\n" + analysis.generate_ascii_bar_chart(summary["category_breakdown"]))

    # Table breakdown
    print("\n  CATEGORY BREAKDOWN TABLE:")
    print(f"  {'Category':<16} | {'Spent (INR)':>12} | {'Share %':>8} | {'Transactions':>12}")
    print("  " + "-" * 56)
    for cat, data in summary["category_breakdown"].items():
        print(f"  {cat:<16} | ₹{data['total']:>10,.2f} | {data['percentage']:>7.1f}% | {data['count']:>12}")
    print("=" * 70)


def decision_tree_alerts_flow():
    """Activity 5 & 7: Decision Tree Alerts & Data Insights."""
    records = expenses.get_all_expenses()
    monthly_budget, _ = storage.load_budget()
    summary = analysis.calculate_budget_summary(monthly_budget, records)

    print("\n" + "=" * 70)
    print("    DECISION TREE BUDGET ALERTS & ANOMALY DETECTION (ACTIVITY 5)")
    print("=" * 70)
    print(f" Current Status:  {summary['badge']} {summary['status']}")
    print(f" Alert Trigger:   {summary['warning_msg']}")
    print("-" * 70)

    # Anomaly Detection Output
    print("\n--- Spending Anomaly Detection Engine ---")
    anomalies = summary["anomalies"]
    if not anomalies:
        print("  [OK] No spending anomalies detected. All transaction amounts are within bounds.")
    else:
        print(f"  [!] {len(anomalies)} Anomaly Flag(s) Detected:")
        for anom in anomalies:
            print(f"      • Expense #{anom['id']} ({anom['category']} - {anom['description']}): ₹{anom['amount']:,.2f}")
            print(f"        -> {anom['reason']}")

    # Strategic Insights Output
    print("\n--- Data Interpretation Insights (Activity 7) ---")
    insights = analysis.generate_data_insights(summary)
    for item in insights:
        print(f"  {item}")
    print("=" * 70)


def oop_demonstration_flow():
    """Activity 6: Demonstrates Object Modeling, Encapsulation & Inheritance."""
    print("\n" + "=" * 70)
    print("          OBJECT MODELING WITH PAPER CARDS (ACTIVITY 6)")
    print("=" * 70)
    print(" Demonstrating Encapsulation, Polymorphism, and Inheritance in Python:\n")

    exp_objects = expenses.get_all_expense_objects()
    print(" 1. Instantiated Domain Objects (Expense base class with Encapsulation):")
    for obj in exp_objects[:3]:
        print(f"    • {obj.get_summary()}")

    print("\n 2. Inheritance & Polymorphism Demo (RecurringExpense subclass):")
    recurring_sample = RecurringExpense(
        expense_id=99,
        date_str="01-Nov-2026",
        category="Bills",
        description="Hostel Wi-Fi Subscription",
        amount=899.0,
        frequency="Monthly"
    )
    print(f"    • Subclass Instance: {recurring_sample.get_summary()}")
    print(f"      Calculated Annual Projection: ₹{recurring_sample.get_annual_projection():,.2f}")
    print("=" * 70)


def executive_summary_flow():
    """Outputs the combined summary."""
    records = expenses.get_all_expenses()
    monthly_budget, _ = storage.load_budget()
    summary = analysis.calculate_budget_summary(monthly_budget, records)

    print("\n" + "#" * 65)
    print("       MILESTONE 1 & 2 - PROTOTYPE OUTPUT SUMMARY")
    print("#" * 65)
    print(f"  {'Metric':<28} | {'Value'}")
    print("-" * 65)
    print(f"  {'Monthly Budget':<28} | ₹{summary['monthly_budget']:,.2f}")
    print(f"  {'Total Expenses':<28} | ₹{summary['total_expenses']:,.2f}")
    print(f"  {'Remaining Budget':<28} | ₹{summary['remaining_budget']:,.2f}")
    print(f"  {'Budget Used':<28} | {summary['budget_used_pct']:.0f}%")
    print(f"  {'Status':<28} | {summary['status']} {summary['badge']}")
    print(f"  {'Highest Spending Category':<28} | {summary['highest_spending_category']} (₹{summary['highest_category_spent']:,.2f})")
    print("#" * 65)
    print(f"  Alert: {summary['warning_msg']}")
    print("#" * 65)


def reset_prototype_data():
    """Populates prototype data from Milestone document."""
    confirm = input("This will reset expenses to the default sample dataset. Continue? (y/N): ").strip().lower()
    if confirm != "y":
        print("Reset canceled.")
        return

    sample_expenses = [
        {"id": 1, "date": "01-Oct-2026", "category": "Food", "description": "Lunch", "amount": 250.0},
        {"id": 2, "date": "02-Oct-2026", "category": "Travel", "description": "Metro", "amount": 100.0},
        {"id": 3, "date": "03-Oct-2026", "category": "Shopping", "description": "Clothes", "amount": 1500.0},
        {"id": 4, "date": "04-Oct-2026", "category": "Food", "description": "Dinner", "amount": 400.0},
    ]
    storage.save_expenses(sample_expenses)
    storage.save_budget(15000.0)
    print("\n[SUCCESS] Sample data loaded successfully!")
    print("  Monthly Budget: ₹15,000.00")
    print("  4 Expenses loaded totaling ₹2,250.00")


def main():
    storage.initialize_storage()
    print_banner()

    while True:
        try:
            print_menu()
            choice = input("Enter choice (0-10): ").strip()
            if choice == "1":
                view_all_expenses()
            elif choice == "2":
                add_expense_flow()
            elif choice == "3":
                edit_expense_flow()
            elif choice == "4":
                delete_expense_flow()
            elif choice == "5":
                budget_flow()
            elif choice == "6":
                visual_spending_analysis_flow()
            elif choice == "7":
                decision_tree_alerts_flow()
            elif choice == "8":
                oop_demonstration_flow()
            elif choice == "9":
                executive_summary_flow()
            elif choice == "10":
                reset_prototype_data()
            elif choice == "0":
                print("\nThank you for using Expense & Budget Analyzer! Goodbye.")
                sys.exit(0)
            else:
                print("[WARNING] Invalid choice. Please choose an option between 0 and 10.")
        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting cleanly.")
            sys.exit(0)


if __name__ == "__main__":
    main()
