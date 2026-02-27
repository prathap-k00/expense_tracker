"""
Category management routes - CRUD for expense categories.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.category import Category

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/')
@login_required
def list_categories():
    """List all categories for current user."""
    categories = Category.query.filter_by(
        user_id=current_user.user_id
    ).order_by(Category.category_name).all()
    
    return render_template('categories/list.html', categories=categories)

@categories_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add new category."""
    if request.method == 'POST':
        name = request.form.get('category_name', '').strip()
        
        if not name or len(name) < 2:
            flash('Category name must be at least 2 characters.', 'danger')
            return render_template('categories/form.html')
        
        existing = Category.query.filter_by(
            user_id=current_user.user_id,
            category_name=name
        ).first()
        
        if existing:
            flash(f'Category "{name}" already exists.', 'warning')
            return render_template('categories/form.html')
        
        category = Category(user_id=current_user.user_id, category_name=name)
        db.session.add(category)
        db.session.commit()
        flash(f'Category "{name}" added successfully!', 'success')
        return redirect(url_for('categories.list_categories'))
    
    return render_template('categories/form.html')

@categories_bp.route('/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete category - expenses in this category will be affected (CASCADE)."""
    category = Category.query.filter_by(
        category_id=category_id,
        user_id=current_user.user_id
    ).first_or_404()
    
    name = category.category_name
    db.session.delete(category)
    db.session.commit()
    flash(f'Category "{name}" deleted. Related expenses were also removed.', 'info')
    return redirect(url_for('categories.list_categories'))
