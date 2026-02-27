"""
User model - Handles user authentication and profile data.
Implements Flask-Login's UserMixin for session management.
"""

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    """
    User table - stores registered user information.
    Each user can only access their own financial data.
    """
    __tablename__ = 'users'
    
    # Primary key
    user_id = db.Column(db.Integer, primary_key=True)
    
    # User credentials and profile
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Timestamp for account creation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - cascade delete ensures user data is removed when user is deleted
    categories = db.relationship('Category', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    income_records = db.relationship('Income', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    # Flask-Login requires 'id' attribute
    @property
    def id(self):
        return self.user_id
    
    def set_password(self, password):
        """Hash and store password - never store plain text passwords."""
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verify password against stored hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'
