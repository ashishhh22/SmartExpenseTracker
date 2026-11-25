"""
Script to generate the comprehensive Milestone 2 Project Report in Microsoft Word (.docx) format.
Covers Experiential Learning Activities 3 to 7 with academic styling, professional color palette,
tables, callout boxes, and viva reference material.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_table(table, col_widths, header_bg="1F4E79", alt_bg="F2F5F9"):
    """Applies professional borders, alignments, and alternating row backgrounds to a table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, cell in enumerate(table.rows[0].cells):
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=140, bottom=140, left=160, right=160)
        for p in cell.paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)
                run.font.size = Pt(10)
    
    # Body rows
    for r_idx, row in enumerate(table.rows[1:], start=1):
        bg = alt_bg if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9.5)
                    run.font.color.rgb = RGBColor(40, 40, 40)
                    
    # Column widths
    for row in table.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = Inches(w)

def add_callout(doc, text, title="NOTE / KEY INSIGHT", border_color="2E75B6", bg_color="EBF1F5"):
    """Creates a distinct styled callout box in the Word document."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.color.rgb = RGBColor(31, 78, 121)
    run_t.font.size = Pt(10)
    
    run_b = p.add_run(text)
    run_b.font.size = Pt(9.5)
    run_b.font.italic = True
    run_b.font.color.rgb = RGBColor(50, 50, 50)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_report():
    doc = Document()
    
    # Page setup: Standard 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    navy = RGBColor(31, 78, 121)
    slate = RGBColor(46, 117, 182)
    charcoal = RGBColor(40, 40, 40)

    # ==================== COVER / HEADER ====================
    p_header = doc.add_paragraph()
    p_header.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_uni = p_header.add_run("B.TECH COMPUTER SCIENCE & ENGINEERING\nEXPERIENTIAL LEARNING COLLABORATIVE PROJECT REPORT\n")
    r_uni.font.size = Pt(11)
    r_uni.font.bold = True
    r_uni.font.color.rgb = slate

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("Expense & Budget Analyzer")
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = navy

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("Milestone 2 Comprehensive Report: Experiential Learning Activities 3 to 7 Integration")
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(90, 90, 90)

    # Team Members Table
    team_table = doc.add_table(rows=5, cols=3)
    team_headers = ["Team Member", "Module / Area", "Core Milestone Responsibilities"]
    for i, h in enumerate(team_headers):
        team_table.cell(0, i).paragraphs[0].text = h
        
    team_data = [
        ("Jiya", "Expense Management (expenses.py)", "Record validation, addition, mutation, deletion, and domain model mapping."),
        ("Ashish", "CSV Data Storage (storage.py)", "Persistent CSV schema maintenance, atomic file writing, reader/dict serialization."),
        ("Garv", "Budget & Analytics (analysis.py)", "Decision tree alert logic, hash-table category summaries, anomaly detection."),
        ("Shreya", "Integration & UI (main.py)", "Application lifecycle, CLI workflows, CRC synthesis, testing, and documentation.")
    ]
    for r_idx, row in enumerate(team_data, start=1):
        for c_idx, val in enumerate(row):
            team_table.cell(r_idx, c_idx).paragraphs[0].text = val
            
    style_table(team_table, [1.5, 2.3, 2.7], header_bg="1F4E79", alt_bg="F7F9FB")
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==================== EXECUTIVE SUMMARY ====================
    h1 = doc.add_heading("Executive Summary & Milestone 2 Context", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.runs[0].font.color.rgb = navy

    doc.add_paragraph(
        "This project report details the comprehensive development and academic synthesis of the Expense & Budget Analyzer, "
        "a modular personal-finance tracking software engineered in Python. In accordance with course guidelines, Experiential "
        "Learning (EL) Activities 1 and 2 were submitted separately. This Milestone 2 submission executes and embeds the remaining "
        "five activities (Activities 3 through 7) directly within the engineering lifecycle of our collaborative software application."
    )

    doc.add_paragraph(
        "By grounding each learning activity in a concrete software implementation, our team bridged high-level system analysis "
        "with robust algorithmic modeling: decomposing real-world constraints into isolated functions (Activity 3), justifying "
        "algorithmic choices via card sorting (Activity 4), designing multi-tiered decision trees (Activity 5), enforcing object "
        "invariants and inheritance hierarchies with CRC modeling (Activity 6), and conducting quantitative data interpretation on "
        "live application outputs (Activity 7)."
    )

    add_callout(
        doc,
        "All functionalities described in this report are fully integrated into our runnable Python application. "
        "The project runs without external dependencies, utilizing Python's built-in standard library with structured CSV file persistence.",
        title="IMPLEMENTATION ASSURANCE"
    )

    # ==================== ACTIVITY 3 ====================
    h1 = doc.add_heading("1. Activity 3: Problem Decomposition Workshop", level=1)
    h1.runs[0].font.color.rgb = navy
    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Evidence Integration Area: Problem Identification and Project Documentation")
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_heading("1.1 Real-World Problem Decomposition", level=2)
    doc.add_paragraph(
        "Managing personal finances is a pervasive challenge for college students and entry-level professionals. "
        "Through our problem decomposition workshop, we unbundled this broad challenge into four discrete root sub-problems:"
    )
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Unstructured Micro-Transactions: ").bold = True
    p.add_run("Small daily outlays (e.g., snacks, local transit) are omitted from mental accounting, causing sudden budget exhaustion.")
    
    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Missing Categorization Boundaries: ").bold = True
    p.add_run("Users lack clarity on whether capital is spent on essential needs (food, utilities) or discretionary wants (shopping, entertainment).")

    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Delayed Retrospective Feedback: ").bold = True
    p.add_run("Traditional monthly reviews occur only after funds have been exhausted, preventing proactive spending interventions.")

    p = doc.add_paragraph(style='List Bullet')
    p.add_run("Friction in Tool Adoption: ").bold = True
    p.add_run("Commercial banking apps introduce high cognitive load and security concerns regarding bank account linking.")

    doc.add_heading("1.2 Hierarchical Architectural Decomposition", level=2)
    doc.add_paragraph(
        "To address these sub-problems systematically, the Expense & Budget Analyzer was structured into five distinct, "
        "loosely coupled architectural layers:"
    )
    
    layers = [
        ("Layer 1: Persistence Layer (storage.py)", "Manages filesystem storage, schema creation, atomic writes, and CSV record retrieval."),
        ("Layer 2: Domain Entity Layer (models.py)", "Defines object models, data encapsulation invariants, and polymorphic behavior."),
        ("Layer 3: Expense Service Layer (expenses.py)", "Executes transaction validation, record insertion, editing, and deletion."),
        ("Layer 4: Analytical Engine (analysis.py)", "Implements hash-map grouping, decision tree alerts, and ASCII distribution rendering."),
        ("Layer 5: User Interface Layer (main.py)", "Orchestrates interactive menu workflows, formatted reports, and exception handling.")
    ]
    for title, desc in layers:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{title}: ").bold = True
        p.add_run(desc)

    doc.add_heading("1.3 Functional Decomposition & Single-Responsibility Mapping", level=2)
    doc.add_paragraph(
        "Each functional module was partitioned into isolated Python functions adhering strictly to the Single Responsibility Principle (SRP):"
    )

    decomp_table = doc.add_table(rows=7, cols=5)
    decomp_headers = ["Module", "Function Name", "Input Parameters", "Return Type", "Single Responsibility Justification"]
    for i, h in enumerate(decomp_headers):
        decomp_table.cell(0, i).paragraphs[0].text = h

    decomp_rows = [
        ("storage.py", "load_expenses()", "None", "list[dict]", "Pure I/O: extracts records from CSV without business evaluation."),
        ("storage.py", "save_expenses()", "expenses: list[dict]", "None", "Atomic persistence: overwrites CSV with updated record state."),
        ("models.py", "Expense.amount", "value: float/str", "None (setter)", "Invariant enforcement: validates amount is strictly greater than 0."),
        ("models.py", "Budget.evaluate_status()", "total_spent: float", "dict", "Decision logic: maps consumption ratio to multi-tier health status."),
        ("expenses.py", "validate_date()", "date_str: str", "str or None", "Sanitization: parses multi-format strings into normalized DD-Mon-YYYY."),
        ("analysis.py", "calculate_category_breakdown()", "expenses: list", "dict", "Aggregation: groups records into categories with percentage shares.")
    ]
    for r_idx, row in enumerate(decomp_rows, start=1):
        for c_idx, val in enumerate(row):
            decomp_table.cell(r_idx, c_idx).paragraphs[0].text = val

    style_table(decomp_table, [1.1, 1.4, 1.2, 1.0, 1.8], header_bg="1F4E79")
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==================== ACTIVITY 4 ====================
    h1 = doc.add_heading("2. Activity 4: Card Sorting Activity & Algorithmic Analysis", level=1)
    h1.runs[0].font.color.rgb = navy
    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Evidence Integration Area: Project Documentation, PPT and Viva")
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_heading("2.1 Information Architecture & Taxonomy", level=2)
    doc.add_paragraph(
        "Card sorting was conducted to structure the system's mental model, cluster user interactions, and establish "
        "an intuitive taxonomic hierarchy:"
    )

    cs_table = doc.add_table(rows=5, cols=3)
    cs_headers = ["Taxonomy Cluster", "Identified Information Cards", "System Functional Role"]
    for i, h in enumerate(cs_headers):
        cs_table.cell(0, i).paragraphs[0].text = h

    cs_data = [
        ("User Inputs", "Transaction Date, Category, Description, Monetary Amount, Monthly Budget Limit", "Raw telemetry captured from the user during transaction logging."),
        ("Business Processes", "Format Normalization, Positivity Validation, Category Grouping, Outlier Flagging", "Transformation algorithms executing business policies and calculations."),
        ("System Modules", "Storage Engine, Domain Entity Layer, Expense Manager, Analytical Dashboard", "Modular code components encapsulating bounded application contexts."),
        ("Output Artifacts", "Tabular Logs, Category Share %, ASCII Distribution Charts, Budget Alert Badges", "Human-readable visual reports and financial telemetry presented to users.")
    ]
    for r_idx, row in enumerate(cs_data, start=1):
        for c_idx, val in enumerate(row):
            cs_table.cell(r_idx, c_idx).paragraphs[0].text = val

    style_table(cs_table, [1.4, 2.5, 2.6], header_bg="1F4E79")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading("2.2 Algorithmic Approaches: Comparison & Justification", level=2)
    doc.add_paragraph(
        "During system synthesis, our team evaluated alternative algorithmic options across core functions, "
        "justifying our final architectural decisions based on asymptotic complexity and application constraints:"
    )

    algo_table = doc.add_table(rows=4, cols=5)
    algo_headers = ["Functional Area", "Candidate Algorithms", "Time Complexity", "Space Complexity", "Engineering Justification"]
    for i, h in enumerate(algo_headers):
        algo_table.cell(0, i).paragraphs[0].text = h

    algo_data = [
        ("Data Persistence", "1. SQLite Relational DB\n2. JSON Object Tree\n3. CSV Flat File (Selected)", "O(N) Read\nO(N) Write", "O(N)", "CSV provides zero-dependency, human-auditable persistence directly compatible with Microsoft Excel."),
        ("Category Aggregation", "1. Nested Category Loops\n2. Sorting + Linear Scan\n3. Hash Accumulator (Selected)", "Nested: O(N*K)\nSort: O(N log N)\nHash: O(N)", "O(K)", "Utilizing collections.defaultdict enables a single-pass O(N) linear aggregation with O(1) amortized bucket updates."),
        ("Anomaly Detection", "1. Static Fixed Threshold\n2. Interquartile Range (IQR)\n3. Mean Multiplier (Selected)", "IQR: O(N log N)\nMean Mult: O(N)", "O(1)", "Flagging transactions where Amount >= 2.5 * Mean provides intuitive, outlier detection in O(N) time.")
    ]
    for r_idx, row in enumerate(algo_data, start=1):
        for c_idx, val in enumerate(row):
            algo_table.cell(r_idx, c_idx).paragraphs[0].text = val

    style_table(algo_table, [1.3, 1.5, 1.2, 0.9, 1.6], header_bg="1F4E79")
    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==================== ACTIVITY 5 ====================
    h1 = doc.add_heading("3. Activity 5: Decision Tree Design", level=1)
    h1.runs[0].font.color.rgb = navy
    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Evidence Integration Area: Project Documentation and Project Demonstration")
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_heading("3.1 Multi-Tier Budget Health Decision Tree", level=2)
    doc.add_paragraph(
        "To prevent delayed financial feedback, our application implements a hierarchical decision-tree control workflow. "
        "The engine computes the budget consumption percentage P = (Total Spent / Monthly Budget) * 100 and classifies financial health:"
    )

    dt_table = doc.add_table(rows=5, cols=4)
    dt_headers = ["Condition / Predicate", "Health State", "Visual Badge", "Triggered Action & System Advisory"]
    for i, h in enumerate(dt_headers):
        dt_table.cell(0, i).paragraphs[0].text = h

    dt_data = [
        ("Total Spent > Monthly Budget", "Budget Exceeded", "[CRITICAL BREACH]", "Triggers high-priority warning alerting user of the exact deficit amount in INR."),
        ("90.0% <= Usage < 100.0%", "Critical (Near Limit)", "[CRITICAL WARNING]", "Advises an immediate emergency spending freeze; highlights danger of imminent breach."),
        ("75.0% <= Usage < 90.0%", "Approaching Limit", "[CAUTION]", "Cautions user to restrict non-essential purchases; displays remaining runway."),
        ("Usage < 75.0%", "Within Budget", "[SAFE / ON TRACK]", "Confirms healthy cash-flow trajectory and prints safe available balance.")
    ]
    for r_idx, row in enumerate(dt_data, start=1):
        for c_idx, val in enumerate(row):
            dt_table.cell(r_idx, c_idx).paragraphs[0].text = val

    style_table(dt_table, [1.6, 1.4, 1.5, 2.0], header_bg="1F4E79")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading("3.2 Spending Anomaly & Outlier Decision Logic", level=2)
    doc.add_paragraph(
        "In addition to global budget monitoring, individual transactions are evaluated by an automated anomaly decision rule:"
    )
    doc.add_paragraph(
        "Let mu be the mean expenditure across all logged transactions. For each record j:\n"
        "IF Amount(j) >= 2.5 * mu THEN Flag Transaction as Statistical Outlier\n"
        "ELSE Treat as Normal Operational Expense."
    )
    add_callout(
        doc,
        "In our Milestone test dataset (mean spend = ₹562.50), Expense #3 (Clothes - ₹1,500.00) is 2.7x the mean spend, "
        "successfully triggering an anomaly alert without requiring external statistical libraries.",
        title="DECISION TREE VALIDATION"
    )

    # ==================== ACTIVITY 6 ====================
    h1 = doc.add_heading("4. Activity 6: Object Modeling with Paper Cards", level=1)
    h1.runs[0].font.color.rgb = navy
    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Evidence Integration Area: Project Documentation, PPT and Viva")
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_heading("4.1 Class-Responsibility-Collaborator (CRC) Cards", level=2)
    doc.add_paragraph(
        "Using paper cards during design sprints, we identified domain entities, demarcated responsibilities, and defined collaborators:"
    )

    # CRC Table 1
    crc1 = doc.add_table(rows=4, cols=2)
    crc1.cell(0, 0).paragraphs[0].text = "Class: Expense"
    crc1.cell(0, 1).paragraphs[0].text = "Superclass: None"
    crc1.cell(1, 0).paragraphs[0].text = "Responsibilities:\n• Maintain transaction id, date, category, desc, amount.\n• Enforce input invariants (positive amounts, valid dates).\n• Serialize state to dictionary format (to_dict()).\n• Return formatted polymorphic string representation."
    crc1.cell(1, 1).paragraphs[0].text = "Collaborators:\n• storage.py\n• datetime parser\n• BudgetAnalyzer"
    style_table(crc1, [3.2, 3.3], header_bg="2E75B6")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # CRC Table 2
    crc2 = doc.add_table(rows=4, cols=2)
    crc2.cell(0, 0).paragraphs[0].text = "Class: RecurringExpense"
    crc2.cell(0, 1).paragraphs[0].text = "Superclass: Expense (Inheritance)"
    crc2.cell(1, 0).paragraphs[0].text = "Responsibilities:\n• Inherit all base validation and state from Expense.\n• Maintain recurrence cadence (Daily, Weekly, Monthly, Yearly).\n• Calculate annual financial commitment.\n• Override get_summary() with recurring metadata."
    crc2.cell(1, 1).paragraphs[0].text = "Collaborators:\n• Expense (Superclass)\n• BudgetAnalyzer"
    style_table(crc2, [3.2, 3.3], header_bg="2E75B6")
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # CRC Table 3
    crc3 = doc.add_table(rows=4, cols=2)
    crc3.cell(0, 0).paragraphs[0].text = "Class: Budget"
    crc3.cell(0, 1).paragraphs[0].text = "Superclass: None"
    crc3.cell(1, 0).paragraphs[0].text = "Responsibilities:\n• Encapsulate monthly allocation and category ceilings.\n• Compute remaining financial runway and consumption %.\n• Execute four-tier health decision tree evaluation."
    crc3.cell(1, 1).paragraphs[0].text = "Collaborators:\n• Expense\n• storage.py"
    style_table(crc3, [3.2, 3.3], header_bg="2E75B6")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading("4.2 Demonstration of Object-Oriented Pillars in Python", level=2)
    oop_pillars = [
        ("Encapsulation", "In models.py, attributes (_amount, _date, _category) are strictly protected. Mutations pass through @property setters that enforce integrity rules, rejecting negative amounts or corrupted date formats before state changes can persist."),
        ("Inheritance", "RecurringExpense inherits core behavior from Expense via super().__init__(...). This eliminates redundant code while extending capabilities with billing frequency and projected annual liability calculation."),
        ("Polymorphism", "RecurringExpense overrides get_summary(). When iterating over a heterogeneous collection of Expense and RecurringExpense objects, Python dynamically resolves the appropriate method implementation at runtime."),
        ("Data Abstraction", "High-level analytics and UI modules interact exclusively with clean domain entity interfaces, completely decoupled from underlying CSV parsing and disk persistence routines.")
    ]
    for name, desc in oop_pillars:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{name}: ").bold = True
        p.add_run(desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==================== ACTIVITY 7 ====================
    h1 = doc.add_heading("5. Activity 7: Data Interpretation Challenge", level=1)
    h1.runs[0].font.color.rgb = navy
    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Evidence Integration Area: Project Documentation and Project Demonstration")
    r.font.italic = True
    r.font.color.rgb = slate

    doc.add_heading("5.1 Quantitative Output Dataset Analysis", level=2)
    doc.add_paragraph(
        "To demonstrate real data interpretation, the application was evaluated using the Milestone benchmark dataset:"
    )

    data_table = doc.add_table(rows=6, cols=6)
    data_headers = ["ID", "Date", "Category", "Description", "Amount (INR)", "Expenditure Share"]
    for i, h in enumerate(data_headers):
        data_table.cell(0, i).paragraphs[0].text = h

    data_rows = [
        ("#1", "01-Oct-2026", "Food", "Lunch", "₹250.00", "11.1%"),
        ("#2", "02-Oct-2026", "Travel", "Metro", "₹100.00", "4.4%"),
        ("#3", "03-Oct-2026", "Shopping", "Clothes", "₹1,500.00", "66.7%"),
        ("#4", "04-Oct-2026", "Food", "Dinner", "₹400.00", "17.8%"),
        ("TOTAL", "Oct 1 - 4", "3 Categories", "4 Transactions", "₹2,250.00", "100.0%")
    ]
    for r_idx, row in enumerate(data_rows, start=1):
        for c_idx, val in enumerate(row):
            data_table.cell(r_idx, c_idx).paragraphs[0].text = val

    style_table(data_table, [0.6, 1.2, 1.2, 1.4, 1.1, 1.0], header_bg="1F4E79")
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading("5.2 Performance Visualization: Category Distribution", level=2)
    doc.add_paragraph(
        "Our analytical engine renders a visual ASCII distribution chart directly in the console environment, "
        "translating raw expenditure values into proportioned Unicode blocks:"
    )

    # Code block formatting for ASCII chart
    chart_text = (
        "  +-------------------------------------------------------------+\n"
        "  | CATEGORY SPENDING DISTRIBUTION (ASCII VISUALIZATION)         |\n"
        "  +-------------------------------------------------------------+\n"
        "  | Shopping  | [█████████████████░░░░░░░░]  66.7% (₹1,500.00) |\n"
        "  | Food      | [███████░░░░░░░░░░░░░░░░░░]  28.9% (₹  650.00) |\n"
        "  | Travel    | [█░░░░░░░░░░░░░░░░░░░░░░░░]   4.4% (₹  100.00) |\n"
        "  +-------------------------------------------------------------+"
    )
    p_code = doc.add_paragraph()
    r_code = p_code.add_run(chart_text)
    r_code.font.name = "Consolas"
    r_code.font.size = Pt(8.5)
    r_code.font.color.rgb = RGBColor(30, 30, 30)

    doc.add_heading("5.3 Key Data Patterns & Strategic Financial Insights", level=2)
    insights = [
        ("Pareto Principle (80/20 Rule)", "A single discretionary purchase (Clothes - ₹1,500.00) constitutes 66.7% of total capital outlay. Combined with Food, two categories represent 95.6% of spending, verifying that expenditure is dominated by lifestyle discretionary choices rather than routine overhead."),
        ("Burn-Rate & Runway Analysis", "Total expenditure of ₹2,250 over 4 days represents a gross daily burn rate of ₹562.50. Extrapolating linearly over a 30-day month yields ₹16,875 (exceeding the ₹15,000 budget). However, filtering out the non-recurring clothing purchase reveals an essential burn rate of only ₹187.50/day (projected ₹5,625/month), affirming that the underlying baseline is healthy."),
        ("Anomaly Flag Confirmation", "The automated detection engine successfully flagged Expense #3 as an outlier at 2.7x mean spend, validating our decision-tree algorithm without manual supervisory intervention.")
    ]
    for title, body in insights:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{title}: ").bold = True
        p.add_run(body)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==================== VIVA & PPT GUIDE ====================
    h1 = doc.add_heading("6. Viva Voce & Presentation (PPT) Quick Reference", level=1)
    h1.runs[0].font.color.rgb = navy

    doc.add_heading("6.1 Slide-by-Slide Outline for Milestone 2 Presentation", level=2)
    slides = [
        ("Slide 1: Title & Overview", "Project title, team member responsibilities, and Milestone 2 scope."),
        ("Slide 2: Problem Decomposition (Act. 3)", "Deconstruction of student finance challenges and 5-tier functional architecture."),
        ("Slide 3: Card Sorting & Algorithms (Act. 4)", "Taxonomy matrix; justification of O(N) hash grouping and CSV storage over SQL."),
        ("Slide 4: Decision Tree Design (Act. 5)", "Multi-tier budget alert flowchart (Safe, Caution, Critical, Breach) and anomaly rule."),
        ("Slide 5: Object Modeling (Act. 6)", "CRC cards, UML class diagram, Encapsulation with @property, and RecurringExpense inheritance."),
        ("Slide 6: Data Interpretation (Act. 7)", "Visual ASCII chart, Pareto 80/20 breakdown, burn-rate metrics, and strategic recommendations.")
    ]
    for s_title, s_desc in slides:
        p = doc.add_paragraph(style='List Bullet')
        p.add_run(f"{s_title}: ").bold = True
        p.add_run(s_desc)

    doc.add_heading("6.2 High-Yield Viva Questions and Model Answers", level=2)
    viva_qa = [
        ("Q1: Why did your team select CSV storage over SQLite for this milestone?",
         "Answer: CSV satisfies the core project specifications with zero external dependencies, provides immediate human audibility, enables direct Excel interoperability, and incurs minimal runtime overhead for student-level transaction volumes."),
        ("Q2: How is Encapsulation demonstrated in your codebase?",
         "Answer: In models.py, the Expense class protects attributes (_amount, _date) and restricts direct mutations. The @amount.setter rejects negative or non-numerical values, safeguarding object state integrity."),
        ("Q3: What makes your category aggregation algorithm optimal?",
         "Answer: By leveraging collections.defaultdict, we achieve O(N) linear time complexity with O(1) amortized hash updates, outperforming nested category scanning which requires O(N * K) comparisons."),
        ("Q4: How does the application detect spending anomalies?",
         "Answer: It computes the dynamic sample mean of all logged transactions and flags any expense whose amount is at least 2.5 times the mean, catching high-ticket outliers automatically.")
    ]
    for q, a in viva_qa:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r_q = p.add_run(q)
        r_q.bold = True
        r_q.font.color.rgb = navy
        
        p_ans = doc.add_paragraph()
        p_ans.paragraph_format.space_after = Pt(6)
        r_a = p_ans.add_run(a)
        r_a.font.size = Pt(9.5)

    # Save document
    output_filename = "Expense_and_Budget_Analyzer_Milestone_2_Report.docx"
    doc.save(output_filename)
    print(f"[SUCCESS] Word report successfully created at: {output_filename}")

if __name__ == "__main__":
    build_report()
