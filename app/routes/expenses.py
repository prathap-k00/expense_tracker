"""
Expense management routes - CRUD operations for expenses.
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import extract
from app import db
from app.models.expense import Expense
from app.models.category import Category

expenses_bp = Blueprint('expenses', __name__)

def get_user_categories():
    """Helper to get categories for current user."""
    return Category.query.filter_by(user_id=current_user.user_id).order_by(Category.category_name).all()

@expenses_bp.route('/')
@login_required
def list_expenses():
    """List all expenses for current user with optional filters."""
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', type=int)
    month_filter = request.args.get('month', type=int)
    year_filter = request.args.get('year', type=int)
    
    query = Expense.query.filter_by(user_id=current_user.user_id)
    
    if category_filter:
        query = query.filter_by(category_id=category_filter)
    if month_filter:
        query = query.filter(extract('month', Expense.expense_date) == month_filter)
    if year_filter:
        query = query.filter(extract('year', Expense.expense_date) == year_filter)
    
    expenses = query.order_by(Expense.expense_date.desc()).paginate(page=page, per_page=10)
    
    return render_template(
        'expenses/list.html',
        expenses=expenses,
        categories=get_user_categories()
    )

@expenses_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    """Add new expense with validation."""
    categories = get_user_categories()
    if not categories:
        flash('Please create at least one category first.', 'warning')
        return redirect(url_for('categories.add_category'))
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            category_id = int(request.form.get('category_id'))
            date_str = request.form.get('expense_date')
            description = request.form.get('description', '').strip()
            
            if amount <= 0:
                flash('Amount must be positive.', 'danger')
                return render_template('expenses/form.html', categories=categories)
            
            # Verify category belongs to user
            category = Category.query.filter_by(
                category_id=category_id,
                user_id=current_user.user_id
            ).first()
            if not category:
                flash('Invalid category selected.', 'danger')
                return render_template('expenses/form.html', categories=categories)
            
            expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            expense = Expense(
                user_id=current_user.user_id,
                category_id=category_id,
                amount=amount,
                expense_date=expense_date,
                description=description
            )
            db.session.add(expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses.list_expenses'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
    
    return render_template('expenses/form.html', categories=categories, expense=None)

@expenses_bp.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    """Edit existing expense - only owner can edit."""
    expense = Expense.query.filter_by(
        expense_id=expense_id,
        user_id=current_user.user_id
    ).first_or_404()
    
    categories = get_user_categories()
    
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            category_id = int(request.form.get('category_id'))
            date_str = request.form.get('expense_date')
            description = request.form.get('description', '').strip()
            
            if amount <= 0:
                flash('Amount must be positive.', 'danger')
                return render_template('expenses/form.html', expense=expense, categories=categories)
            
            category = Category.query.filter_by(
                category_id=category_id,
                user_id=current_user.user_id
            ).first()
            if not category:
                flash('Invalid category selected.', 'danger')
                return render_template('expenses/form.html', expense=expense, categories=categories)
            
            expense.amount = amount
            expense.category_id = category_id
            expense.expense_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            expense.description = description
            db.session.commit()
            flash('Expense updated successfully!', 'success')
            return redirect(url_for('expenses.list_expenses'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
    
    return render_template('expenses/form.html', expense=expense, categories=categories)

@expenses_bp.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    """Delete expense - only owner can delete."""
    expense = Expense.query.filter_by(
        expense_id=expense_id,
        user_id=current_user.user_id
    ).first_or_404()
    
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully.', 'success')
    return redirect(url_for('expenses.list_expenses'))
