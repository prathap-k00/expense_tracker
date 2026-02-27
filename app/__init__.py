"""
Expense Tracker - Main Application Factory
Flask app initialization with extensions and blueprints.
Follows MVC architecture for maintainability.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize extensions (db first, then login_manager)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='default'):
    """
    Application factory pattern - creates and configures the Flask app.
    This allows for different configurations (dev, prod, test).
    """
    app = Flask(__name__)
    
    # Load configuration
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure Flask-Login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader - required by Flask-Login to load user from session
    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints for modular routing
    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.expenses import expenses_bp
    from app.routes.income import income_bp
    from app.routes.categories import categories_bp
    from app.routes.budgets import budgets_bp
    from app.routes.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(expenses_bp, url_prefix='/expenses')
    app.register_blueprint(income_bp, url_prefix='/income')
    app.register_blueprint(categories_bp, url_prefix='/categories')
    app.register_blueprint(budgets_bp, url_prefix='/budgets')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    # Create database tables within app context
    # Import models to register them with SQLAlchemy before create_all()
    with app.app_context():
        from app import models  # noqa: F401
        db.create_all()
    
    return app
