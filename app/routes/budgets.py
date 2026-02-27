"""
Budget management routes - Set and view monthly budgets.
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func, extract
from app import db
from app.models.budget import Budget
from app.models.expense import Expense

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/')
@login_required
def list_budgets():
    """List budgets - show current and recent months."""
    budgets = Budget.query.filter_by(
        user_id=current_user.user_id
    ).order_by(Budget.year.desc(), Budget.month.desc()).limit(12).all()
    
    # Get actual expenses for each budget
    budget_data = []
    for b in budgets:
        spent = db.session.query(func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.user_id,
            extract('month', Expense.expense_date) == b.month,
            extract('year', Expense.expense_date) == b.year
        ).scalar() or 0
        budget_data.append({
            'budget': b,
            'spent': float(spent),
            'remaining': b.amount - float(spent)
        })
    
    return render_template('budgets/list.html', budget_data=budget_data)

@budgets_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_budget():
    """Add or update monthly budget."""
    if request.method == 'POST':
        try:
            month = int(request.form.get('month'))
            year = int(request.form.get('year'))
            amount = float(request.form.get('amount', 0))
            
            if amount <= 0:
                flash('Budget amount must be positive.', 'danger')
                return render_template('budgets/form.html', now=datetime.now())
            if month < 1 or month > 12:
                flash('Invalid month.', 'danger')
                return render_template('budgets/form.html', now=datetime.now())
            
            existing = Budget.query.filter_by(
                user_id=current_user.user_id,
                month=month,
                year=year
            ).first()
            
            if existing:
                existing.amount = amount
                db.session.commit()
                flash(f'Budget for {month}/{year} updated!', 'success')
            else:
                budget = Budget(
                    user_id=current_user.user_id,
                    month=month,
                    year=year,
                    amount=amount
                )
                db.session.add(budget)
                db.session.commit()
                flash(f'Budget for {month}/{year} set successfully!', 'success')
            
            return redirect(url_for('budgets.list_budgets'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
    
    return render_template('budgets/form.html', now=datetime.now())
