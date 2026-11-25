"""
Object Modeling Module (Experiential Learning Activity 6)
Defines domain entities, encapsulation, inheritance, and business behaviors.
"""

from datetime import datetime


class Expense:
    """
    Base domain entity representing an individual financial transaction.
    Demonstrates Encapsulation via private attributes and validated properties.
    """

    def __init__(self, expense_id, date_str, category, description, amount):
        self._id = int(expense_id)
        self.date = date_str
        self.category = category
        self.description = description
        self.amount = amount

    # --- Property: ID ---
    @property
    def id(self):
        return self._id

    # --- Property & Setter: Date ---
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Date must be a non-empty string.")
        # Normalize date
        value = value.strip()
        formats = ["%d-%b-%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
        normalized = None
        for fmt in formats:
            try:
                parsed = datetime.strptime(value, fmt)
                normalized = parsed.strftime("%d-%b-%Y")
                break
            except ValueError:
                continue
        if not normalized:
            raise ValueError(f"Invalid date format '{value}'. Expected DD-Mon-YYYY or YYYY-MM-DD.")
        self._date = normalized

    # --- Property & Setter: Category ---
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value or not str(value).strip():
            self._category = "Others"
        else:
            self._category = str(value).strip().title()

    # --- Property & Setter: Description ---
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not value or not str(value).strip():
            self._description = "General Expense"
        else:
            self._description = str(value).strip()

    # --- Property & Setter: Amount ---
    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        try:
            num = float(value)
            if num <= 0:
                raise ValueError("Amount must be strictly greater than 0.")
            self._amount = round(num, 2)
        except (TypeError, ValueError) as err:
            raise ValueError(f"Invalid amount '{value}': {err}")

    # --- Behaviors & Representation ---
    def get_summary(self):
        """Polymorphic summary method."""
        return f"[#{self._id}] {self._date} | {self._category:<14} | {self._description:<18} | ₹{self._amount:>9,.2f}"

    def to_dict(self):
        """Serialize object to dictionary format for CSV storage."""
        return {
            "id": self._id,
            "date": self._date,
            "category": self._category,
            "description": self._description,
            "amount": self._amount
        }

    @classmethod
    def from_dict(cls, data):
        """Factory method to construct an Expense instance from a dictionary."""
        return cls(
            expense_id=data["id"],
            date_str=data["date"],
            category=data["category"],
            description=data["description"],
            amount=data["amount"]
        )

    def __repr__(self):
        return f"<Expense id={self._id} category='{self._category}' amount={self._amount}>"


class RecurringExpense(Expense):
    """
    Subclass demonstrating INHERITANCE and POLYMORPHISM.
    Extends base Expense with recurring billing frequency and projected annual liability.
    """

    VALID_FREQUENCIES = ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"]

    def __init__(self, expense_id, date_str, category, description, amount, frequency="Monthly"):
        super().__init__(expense_id, date_str, category, description, amount)
        self.frequency = frequency

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        norm = str(value).strip().title()
        if norm not in self.VALID_FREQUENCIES:
            norm = "Monthly"
        self._frequency = norm

    def get_annual_projection(self):
        """Calculates total projected yearly expense for budget forecasting."""
        multipliers = {
            "Daily": 365,
            "Weekly": 52,
            "Monthly": 12,
            "Quarterly": 4,
            "Yearly": 1
        }
        return round(self.amount * multipliers.get(self._frequency, 12), 2)

    def get_summary(self):
        """Method overriding demonstrating Polymorphism."""
        base_str = super().get_summary()
        return f"{base_str} (Recurring: {self._frequency}, Annual: ₹{self.get_annual_projection():,.2f})"


class Budget:
    """
    Domain entity encapsulating budget limits, threshold logic, and status evaluations.
    """

    def __init__(self, monthly_limit=15000.0, category_limits=None):
        self.monthly_limit = monthly_limit
        self._category_limits = category_limits if category_limits is not None else {}

    @property
    def monthly_limit(self):
        return self._monthly_limit

    @monthly_limit.setter
    def monthly_limit(self, value):
        num = float(value)
        if num < 0:
            raise ValueError("Monthly budget limit cannot be negative.")
        self._monthly_limit = round(num, 2)

    @property
    def category_limits(self):
        return dict(self._category_limits)

    def set_category_limit(self, category, limit):
        num = float(limit)
        if num < 0:
            raise ValueError("Category limit cannot be negative.")
        self._category_limits[category.strip().title()] = round(num, 2)

    def calculate_remaining(self, total_spent):
        return round(self._monthly_limit - total_spent, 2)

    def calculate_usage_percentage(self, total_spent):
        if self._monthly_limit <= 0:
            return 0.0
        return round((total_spent / self._monthly_limit) * 100, 2)

    def evaluate_status(self, total_spent):
        """
        Decision Tree evaluation (Activity 5):
        Categorizes budget health into Safe, Approaching, Critical, or Exceeded.
        """
        pct = self.calculate_usage_percentage(total_spent)
        remaining = self.calculate_remaining(total_spent)

        if total_spent > self._monthly_limit:
            return {
                "level": "BREACH",
                "status": "Budget Exceeded",
                "message": f"WARNING: You have exceeded your budget by ₹{abs(remaining):,.2f}!",
                "badge": "[CRITICAL BREACH]"
            }
        elif pct >= 90.0:
            return {
                "level": "CRITICAL",
                "status": "Critical (Near Budget Limit)",
                "message": f"ALERT: You have used {pct:.1f}% of your budget. Only ₹{remaining:,.2f} remaining.",
                "badge": "[CRITICAL WARNING]"
            }
        elif pct >= 75.0:
            return {
                "level": "CAUTION",
                "status": "Approaching Budget Limit",
                "message": f"CAUTION: You have consumed {pct:.1f}% of your budget.",
                "badge": "[CAUTION]"
            }
        else:
            return {
                "level": "SAFE",
                "status": "Within Budget",
                "message": f"Healthy spending: {pct:.1f}% used, ₹{remaining:,.2f} remaining.",
                "badge": "[SAFE / ON TRACK]"
            }
