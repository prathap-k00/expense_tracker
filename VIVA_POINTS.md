# Viva / Interview Explanation Points

Use these points when explaining your project during BCA viva or interviews.

## 1. Project Overview

- **Name**: Expense Tracker with Financial Insights
- **Purpose**: Help users track income and expenses, visualize spending patterns, and receive automated financial insights
- **Target Users**: Individuals managing personal finances

## 2. Technology Choices

| Component | Technology | Reason |
|-----------|------------|--------|
| Backend | Flask | Lightweight, flexible, easy to learn |
| Frontend | HTML, CSS, Bootstrap | No build step, server-rendered |
| Database | SQLite | File-based, no setup, good for projects |
| Charts | Chart.js | Popular, responsive, easy integration |
| Auth | Flask-Login | Handles sessions, login state |

## 3. Architecture (MVC)

- **Model**: SQLAlchemy models (`User`, `Category`, `Expense`, `Income`, `Budget`)
- **View**: Jinja2 templates (HTML with Bootstrap)
- **Controller**: Flask routes/blueprints that handle requests and return responses

## 4. Database Design

- **Normalization**: Each table has a single responsibility
- **Foreign Keys**: `user_id` in all tables ensures data isolation
- **Relationships**: One-to-many (User → Expenses, Category → Expenses)
- **Cascade Delete**: When user is deleted, all related data is removed

## 5. Security Measures

1. **Password Hashing**: `pbkdf2:sha256` - never store plain text
2. **Login Required**: `@login_required` on protected routes
3. **Data Isolation**: All queries filter by `current_user.user_id`
4. **Form Validation**: Server-side validation on all inputs

## 6. Financial Insights Logic

- **Savings %**: (Income - Expense) / Income × 100
- **Overspending**: If current month expense > previous month by 10%
- **Budget Alert**: If expense > budget amount
- **Highest Category**: Identify category with >40% of total expense

## 7. Scalability for AI/ML

- Modular structure with blueprints
- Separate analytics functions in `main.py`
- Could add: expense prediction, anomaly detection, spending recommendations

## 8. Key Code Snippets to Explain

- **User model**: `set_password()`, `check_password()` - password hashing
- **Dashboard**: `get_category_breakdown()`, `get_monthly_expense_trend()` - Chart.js data
- **Financial insights**: `get_financial_insights()` - rule-based insight generation
