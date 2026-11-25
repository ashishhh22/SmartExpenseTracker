# Expense & Budget Analyzer (B.Tech CSE Collaborative Project)

A modular personal-finance system built in Python with CSV-based persistence, object-oriented domain models, decision-tree alerts, and data visualization.

---

## 👥 Team Responsibilities Mapping
| Team Member | Module | Source File | Primary Responsibility |
|---|---|---|---|
| **Jiya** | Expense Management | [expenses.py](file:///d:/CSAE%20project/expense%20and%20budg/expenses.py) | Expense validation, addition, editing, deletion, and domain entity methods. |
| **Ashish** | CSV Data Storage | [storage.py](file:///d:/CSAE%20project/expense%20and%20budg/storage.py) | File persistence, schema initialization, serialization, and deserialization. |
| **Garv** | Budget & Analysis | [analysis.py](file:///d:/CSAE%20project/expense%20and%20budg/analysis.py) | Decision tree budget alerts, category aggregation, and anomaly detection. |
| **Shreya** | Integration, Testing & UI | [main.py](file:///d:/CSAE%20project/expense%20and%20budg/main.py) | Menu-driven console UI, CRC cards synthesis, integration, and documentation. |

---

## 🎯 Experiential Learning Activities Integration (Milestone 2)

As per the course guidelines, Activities 3–7 are integrated into the project:

- **Activity 3 (Problem Decomposition):** Functional decomposition across [storage.py](file:///d:/CSAE%20project/expense%20and%20budg/storage.py), [models.py](file:///d:/CSAE%20project/expense%20and%20budg/models.py), [expenses.py](file:///d:/CSAE%20project/expense%20and%20budg/expenses.py), [analysis.py](file:///d:/CSAE%20project/expense%20and%20budg/analysis.py), and [main.py](file:///d:/CSAE%20project/expense%20and%20budg/main.py).
- **Activity 4 (Card Sorting):** Information taxonomy and algorithmic comparison ($O(N)$ hash-table aggregation vs $O(N \cdot K)$ nested loops).
- **Activity 5 (Decision Tree Design):** Multi-tier budget alert tree (Safe, Caution, Critical, Breach) and statistical outlier anomaly detection ($2.5\times \mu$).
- **Activity 6 (Object Modeling with Paper Cards):** CRC cards, domain entities with Encapsulation (`@property`), Inheritance (`RecurringExpense` extending `Expense`), and Polymorphism (`get_summary()`).
- **Activity 7 (Data Interpretation Challenge):** ASCII distribution bar chart, Pareto 80/20 analysis, daily burn-rate, and financial insights.

Detailed documentation is available in **[Expense_and_Budget_Analyzer_Milestone_2_Report.md](file:///d:/CSAE%20project/expense%20and%20budg/Expense_and_Budget_Analyzer_Milestone_2_Report.md)**.

---

## 🚀 How to Run the Application

1. Open your terminal in this workspace:
   ```bash
   python main.py
   ```
2. Interactive Options:
   - Option `[1]`: View all recorded expenses in formatted tabular layout
   - Option `[2]`: Add a new expense (validated date, category, description, amount)
   - Option `[5]`: View or update monthly budget
   - Option `[6]`: **Activity 7** — Visual Spending Analysis & ASCII Horizontal Bar Chart
   - Option `[7]`: **Activity 5** — Decision Tree Alerts & Anomaly Insights
   - Option `[8]`: **Activity 6** — Object Modeling (Encapsulation, Inheritance & Polymorphism Demo)
   - Option `[9]`: Executive Summary (Milestones 1 & 2 format)
   - Option `[10]`: Reset database to Milestone default prototype data
