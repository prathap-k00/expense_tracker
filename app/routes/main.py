"""
Main routes - Dashboard, home, and financial insights.
Contains analytics logic and Chart.js data.
"""

from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from app import db
from app.models.expense import Expense
from app.models.income import Income
from app.models.budget import Budget
from app.models.category import Category

main_bp = Blueprint('main', __name__)

def get_current_month_data():
    """Get total income and expenses for current month."""
    now = datetime.now()
    income_total = db.session.query(func.sum(Income.amount)).filter(
        Income.user_id == current_user.user_id,
        extract('month', Income.income_date) == now.month,
        extract('year', Income.income_date) == now.year
    ).scalar() or 0
    
    expense_total = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.user_id,
        extract('month', Expense.expense_date) == now.month,
        extract('year', Expense.expense_date) == now.year
    ).scalar() or 0
    
    return float(income_total), float(expense_total)

def get_category_breakdown():
    """Get expense totals per category for current month."""
    now = datetime.now()
    results = db.session.query(
        Category.category_name,
        func.sum(Expense.amount).label('total')
    ).join(Expense).filter(
        Expense.user_id == current_user.user_id,
        extract('month', Expense.expense_date) == now.month,
        extract('year', Expense.expense_date) == now.year
    ).group_by(Category.category_name).all()
    
    return [{'name': r.category_name, 'amount': float(r.total)} for r in results]

def get_monthly_expense_trend(months=6):
    """Get expense totals for last N months for line chart."""
    now = datetime.now()
    data = []
    for i in range(months - 1, -1, -1):
        target_date = now - timedelta(days=30 * i)
        total = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.user_id,
            extract('month', Expense.expense_date) == target_date.month,
            extract('year', Expense.expense_date) == target_date.year
        ).scalar() or 0
        data.append({
            'month': target_date.strftime('%b %Y'),
            'amount': float(total)
        })
    return data

def get_income_vs_expense_data(months=6):
    """Get income and expense totals per month for bar chart comparison."""
    now = datetime.now()
    data = []
    for i in range(months - 1, -1, -1):
        target_date = now - timedelta(days=30 * i)
        income = db.session.query(func.sum(Income.amount)).filter(
            Income.user_id == current_user.user_id,
            extract('month', Income.income_date) == target_date.month,
            extract('year', Income.income_date) == target_date.year
        ).scalar() or 0
        expense = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.user_id,
            extract('month', Expense.expense_date) == target_date.month,
            extract('year', Expense.expense_date) == target_date.year
        ).scalar() or 0
        data.append({
            'month': target_date.strftime('%b %Y'),
            'income': float(income),
            'expense': float(expense),
            'savings': float(income) - float(expense)
        })
    return data

def get_financial_insights():
    """Generate automated text-based financial insights."""
    now = datetime.now()
    insights = []
    
    # Current month totals
    income_total, expense_total = get_current_month_data()
    savings = income_total - expense_total
    savings_pct = (savings / income_total * 100) if income_total > 0 else 0
    
    # Savings percentage insight
    if income_total > 0:
        if savings_pct >= 20:
            insights.append(f"Great job! You're saving {savings_pct:.1f}% of your income this month.")
        elif savings_pct >= 10:
            insights.append(f"Good progress! You're saving {savings_pct:.1f}% - consider increasing to 20%.")
        elif savings_pct > 0:
            insights.append(f"Positive savings ({savings_pct:.1f}%), but try to save at least 10% monthly.")
        else:
            insights.append("Warning: You're spending more than you earn this month. Review expenses.")
    
    # Month-over-month comparison
    if now.month > 1:
        prev_month = now.month - 1
        prev_year = now.year
    else:
        prev_month = 12
        prev_year = now.year - 1
    
    prev_expense = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.user_id,
        extract('month', Expense.expense_date) == prev_month,
        extract('year', Expense.expense_date) == prev_year
    ).scalar() or 0
    prev_expense = float(prev_expense)
    
    if prev_expense > 0 and expense_total > prev_expense * 1.1:
        increase = ((expense_total - prev_expense) / prev_expense) * 100
        insights.append(f"Overspending alert: Expenses are {increase:.1f}% higher than last month.")
    elif prev_expense > 0 and expense_total < prev_expense * 0.9:
        decrease = ((prev_expense - expense_total) / prev_expense) * 100
        insights.append(f"You've reduced spending by {decrease:.1f}% compared to last month!")
    
    # Budget check
    budget = Budget.query.filter_by(
        user_id=current_user.user_id,
        month=now.month,
        year=now.year
    ).first()
    
    if budget and expense_total > budget.amount:
        over = expense_total - budget.amount
        insights.append(f"Budget exceeded by ₹{over:,.2f}. Consider cutting non-essential spending.")
    elif budget and expense_total > budget.amount * 0.9:
        remaining = budget.amount - expense_total
        insights.append(f"Approaching budget limit. ₹{remaining:,.2f} remaining for this month.")
    
    # Highest spending category
    categories = get_category_breakdown()
    if categories:
        top = max(categories, key=lambda x: x['amount'])
        if top['amount'] > expense_total * 0.4 and expense_total > 0:
            pct = (top['amount'] / expense_total) * 100
            insights.append(f"'{top['name']}' is your biggest expense ({pct:.1f}%). Look for ways to optimize.")
    
    return insights

@main_bp.route('/')
def index():
    """Landing page - redirects to dashboard if logged in."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with analytics and charts."""
    income_total, expense_total = get_current_month_data()
    savings = income_total - expense_total
    
    return render_template(
        'dashboard.html',
        income_total=income_total,
        expense_total=expense_total,
        savings=savings,
        category_data=get_category_breakdown(),
        monthly_data=get_monthly_expense_trend(),
        income_vs_expense_data=get_income_vs_expense_data(),
        insights=get_financial_insights()
    )
