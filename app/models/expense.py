"""
Expense model - Individual expense transactions.
Links to user and category for proper data isolation and reporting.
"""

from datetime import datetime
from app import db

class Expense(db.Model):
    """
    Expense table - stores each expense with amount, date, and category.
    Foreign keys ensure referential integrity.
    """
    __tablename__ = 'expenses'
    
    expense_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id', ondelete='CASCADE'), nullable=False)
    
    # Transaction details
    amount = db.Column(db.Float, nullable=False)
    expense_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(200), default='')
    
    def __repr__(self):
        return f'<Expense {self.amount} - {self.expense_date}>'
