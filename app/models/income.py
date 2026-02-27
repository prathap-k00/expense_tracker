"""
Income model - Tracks income sources and amounts.
Used for calculating savings and financial insights.
"""

from app import db

class Income(db.Model):
    """
    Income table - stores income entries with source and date.
    Each user tracks their own income separately.
    """
    __tablename__ = 'income'
    
    income_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    income_date = db.Column(db.Date, nullable=False)
    source = db.Column(db.String(100), default='Salary')
    
    def __repr__(self):
        return f'<Income {self.amount} from {self.source}>'
