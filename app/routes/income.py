"""
Income management routes - Add and view income.
"""

from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.income import Income

income_bp = Blueprint('income', __name__)

@income_bp.route('/')
@login_required
def list_income():
    """List all income entries with pagination."""
    page = request.args.get('page', 1, type=int)
    income_records = Income.query.filter_by(
        user_id=current_user.user_id
    ).order_by(Income.income_date.desc()).paginate(page=page, per_page=10)
    
    return render_template('income/list.html', income_records=income_records)

@income_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_income():
    """Add new income entry."""
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount', 0))
            date_str = request.form.get('income_date')
            source = request.form.get('source', 'Salary').strip() or 'Salary'
            
            if amount <= 0:
                flash('Amount must be positive.', 'danger')
                return render_template('income/form.html')
            
            income_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            income = Income(
                user_id=current_user.user_id,
                amount=amount,
                income_date=income_date,
                source=source
            )
            db.session.add(income)
            db.session.commit()
            flash('Income added successfully!', 'success')
            return redirect(url_for('income.list_income'))
            
        except ValueError as e:
            flash(f'Invalid input: {str(e)}', 'danger')
    
    return render_template('income/form.html')
