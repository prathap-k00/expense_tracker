"""
Budget model - Monthly budget targets per user.
Used for overspending alerts and financial insights.
"""

from app import db

class Budget(db.Model):
    """
    Budget table - stores monthly budget limit per user.
    One budget per user per month-year combination.
    """
    __tablename__ = 'budgets'
    
    budget_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    month = db.Column(db.Integer, nullable=False)  # 1-12
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    
    # Ensure one budget per user per month
    __table_args__ = (
        db.UniqueConstraint('user_id', 'month', 'year', name='unique_user_budget'),
    )
    
    def __repr__(self):
        return f'<Budget {self.month}/{self.year}: {self.amount}>'
