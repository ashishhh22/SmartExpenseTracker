"""
Budget & Analysis Module (Garv - Budget & Analysis)
Experiential Learning Activities 5 (Decision Trees) & 7 (Data Interpretation)

Features:
- Decision Tree logic for multi-tier budget alerts & anomaly detection
- Category breakdown with Pareto 80/20 analysis
- Terminal ASCII performance bar charts for visual data interpretation
- Daily burn-rate calculations and financial insights
"""

from collections import defaultdict
from models import Budget


def _extract_val(record, key):
    """Helper to extract attribute whether record is an Expense object or dict."""
    if hasattr(record, key):
        return getattr(record, key)
    elif isinstance(record, dict) and key in record:
        return record[key]
    raise KeyError(f"Key {key} not found in record.")


def calculate_total_expenses(expenses):
    """Calculate the sum of all recorded expenses."""
    return round(sum(_extract_val(exp, "amount") for exp in expenses), 2)


def calculate_category_breakdown(expenses):
    """
    Calculate expenditure grouped by category.
    Returns:
        dict: {category_name: {"total": float, "percentage": float, "count": int}}
    """
    total = calculate_total_expenses(expenses)
    cat_totals = defaultdict(float)
    cat_counts = defaultdict(int)

    for exp in expenses:
        cat = _extract_val(exp, "category")
        amt = _extract_val(exp, "amount")
        cat_totals[cat] += amt
        cat_counts[cat] += 1

    breakdown = {}
    for cat, amount in sorted(cat_totals.items(), key=lambda x: x[1], reverse=True):
        percentage = (amount / total * 100) if total > 0 else 0.0
        breakdown[cat] = {
            "total": round(amount, 2),
            "percentage": round(percentage, 2),
            "count": cat_counts[cat]
        }

    return breakdown


def get_highest_spending_category(expenses):
    """Find the category with the highest expenditure."""
    breakdown = calculate_category_breakdown(expenses)
    if not breakdown:
        return None, 0.0
    highest_cat = next(iter(breakdown.keys()))
    return highest_cat, breakdown[highest_cat]["total"]


def detect_spending_anomalies(expenses, multiplier_threshold=2.5):
    """
    Decision Tree: Anomaly Detection (Activity 5)
    Flags transactions that significantly deviate from the average transaction amount.
    """
    if len(expenses) < 2:
        return []

    amounts = [_extract_val(e, "amount") for e in expenses]
    avg_amt = sum(amounts) / len(amounts)
    anomalies = []

    for e in expenses:
        amt = _extract_val(e, "amount")
        # Decision Condition: if amount > threshold * average
        if amt >= avg_amt * multiplier_threshold:
            anomalies.append({
                "id": _extract_val(e, "id"),
                "date": _extract_val(e, "date"),
                "category": _extract_val(e, "category"),
                "description": _extract_val(e, "description"),
                "amount": amt,
                "deviation_ratio": round(amt / avg_amt, 1),
                "reason": f"Transaction is {round(amt / avg_amt, 1)}x the average spend of ₹{avg_amt:,.2f}"
            })
    return anomalies


def calculate_budget_summary(monthly_budget, expenses, category_budgets=None):
    """
    Core milestone calculations and Decision Tree status evaluation.
    Utilizes the Budget domain entity.
    """
    budget_obj = Budget(monthly_limit=monthly_budget, category_limits=category_budgets)
    total_expenses = calculate_total_expenses(expenses)
    remaining_budget = budget_obj.calculate_remaining(total_expenses)
    budget_used_pct = budget_obj.calculate_usage_percentage(total_expenses)

    # Decision Tree evaluation via Budget model
    status_info = budget_obj.evaluate_status(total_expenses)

    highest_cat, highest_cat_spent = get_highest_spending_category(expenses)
    category_breakdown = calculate_category_breakdown(expenses)
    anomalies = detect_spending_anomalies(expenses)

    # Calculate average transaction amount
    avg_transaction = round(total_expenses / len(expenses), 2) if expenses else 0.0

    return {
        "monthly_budget": monthly_budget,
        "total_expenses": total_expenses,
        "remaining_budget": remaining_budget,
        "budget_used_pct": budget_used_pct,
        "status": status_info["status"],
        "alert_level": status_info["level"],
        "warning_msg": status_info["message"],
        "badge": status_info["badge"],
        "highest_spending_category": highest_cat,
        "highest_category_spent": highest_cat_spent,
        "category_breakdown": category_breakdown,
        "anomalies": anomalies,
        "avg_transaction": avg_transaction,
        "total_transactions": len(expenses)
    }


def generate_ascii_bar_chart(breakdown, bar_width=25):
    """
    Activity 7: Data Interpretation Visualization
    Generates a visual ASCII horizontal bar chart representing category spending distribution.
    """
    if not breakdown:
        return "No data available for chart generation."

    lines = []
    lines.append("  " + "-" * 65)
    lines.append("  CATEGORY SPENDING DISTRIBUTION (ASCII VISUALIZATION)")
    lines.append("  " + "-" * 65)

    for cat, data in breakdown.items():
        pct = data["percentage"]
        filled_length = int(round(bar_width * pct / 100))
        # Ensure at least 1 block if spending exists
        if filled_length == 0 and pct > 0:
            filled_length = 1
        bar = "█" * filled_length + "░" * (bar_width - filled_length)
        lines.append(f"  {cat:<14} |{bar}| {pct:>5.1f}% (₹{data['total']:>8,.2f})")

    lines.append("  " + "-" * 65)
    return "\n".join(lines)


def generate_data_insights(summary):
    """
    Activity 7: Data Interpretation & Strategic Insights
    Analyzes patterns in spending and provides actionable recommendations.
    """
    insights = []
    pct = summary["budget_used_pct"]
    breakdown = summary["category_breakdown"]
    total = summary["total_expenses"]

    # 1. Budget Health Insight
    if pct > 100:
        insights.append(f"• CRITICAL DEFICIT: Spending has breached the monthly ceiling by ₹{abs(summary['remaining_budget']):,.2f}.")
    elif pct >= 75:
        insights.append(f"• VELOCITY WARNING: Spending has reached {pct:.1f}% of allocation. Recommend freezing discretionary spending.")
    else:
        insights.append(f"• HEALTHY RESERVE: {100 - pct:.1f}% of total budget remains available for the rest of the cycle.")

    # 2. Pareto Category Concentration
    if breakdown:
        top_cat = summary["highest_spending_category"]
        top_data = breakdown[top_cat]
        if top_data["percentage"] >= 50.0:
            insights.append(f"• HIGH CONCENTRATION: '{top_cat}' alone constitutes {top_data['percentage']:.1f}% of all expenses.")
        else:
            insights.append(f"• BALANCED ALLOCATION: Top category '{top_cat}' accounts for {top_data['percentage']:.1f}% of expenses.")

    # 3. Anomaly & Outlier Observation
    anomalies = summary.get("anomalies", [])
    if anomalies:
        insights.append(f"• OUTLIER ALERT: {len(anomalies)} transaction(s) flagged as unusually large (e.g. #{anomalies[0]['id']} {anomalies[0]['description']} - ₹{anomalies[0]['amount']:,.2f}).")
    else:
        insights.append("• CONSISTENT TICKETS: No erratic spending spikes detected; transaction amounts are uniform.")

    return insights
