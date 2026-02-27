"""
Category model - User-defined expense categories.
Each user has their own set of categories (e.g., Food, Transport, Rent).
"""

from app import db

class Category(db.Model):
    """
    Category table - stores expense categories per user.
    Normalized design: one category per row, linked to user.
    """
    __tablename__ = 'categories'
    
    category_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    category_name = db.Column(db.String(50), nullable=False)
    
    # Relationship to expenses - one category has many expenses
    expenses = db.relationship('Expense', backref='category', lazy='dynamic')
    
    # Unique constraint: same user cannot have duplicate category names
    __table_args__ = (
        db.UniqueConstraint('user_id', 'category_name', name='unique_user_category'),
    )
    
    def __repr__(self):
        return f'<Category {self.category_name}>'
