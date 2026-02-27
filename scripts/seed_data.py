"""
Sample data seeding script for Expense Tracker.
Creates a demo user with categories, expenses, income, and budget.
Run: python -m scripts.seed_data (from project root)
"""

import sys
import os
from datetime import datetime, timedelta
from random import choice, randint, uniform

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.user import User
from app.models.category import Category
from app.models.expense import Expense
from app.models.income import Income
from app.models.budget import Budget

def seed_data():
    app = create_app()
    with app.app_context():
        # Check if demo user exists
        if User.query.filter_by(email='demo@expensetracker.com').first():
            print("Demo user already exists. Skipping seed.")
            return

        # Create demo user
        user = User(name='Demo User', email='demo@expensetracker.com')
        user.set_password('demo123')
        db.session.add(user)
        db.session.commit()
        print("Created demo user: demo@expensetracker.com / demo123")

        # Create categories
        category_names = ['Food', 'Transport', 'Rent', 'Utilities', 'Entertainment', 'Shopping', 'Healthcare']
        categories = []
        for name in category_names:
            cat = Category(user_id=user.user_id, category_name=name)
            db.session.add(cat)
            categories.append(cat)
        db.session.commit()
        print(f"Created {len(categories)} categories")

        # Create expenses for last 3 months
        now = datetime.now()
        expense_amounts = [
            (250, 800), (100, 500), (500, 2000), (200, 1500), (50, 300), (100, 1000), (50, 400)
        ]
        descriptions = ['Monthly groceries', 'Fuel', ' rent', 'Electricity bill', 'Movie', 'Clothes', 'Medicine']

        for month_offset in range(3):
            base_date = now - timedelta(days=30 * month_offset)
            year, month = base_date.year, base_date.month
            for _ in range(randint(8, 15)):
                cat_idx = randint(0, len(categories) - 1)
                lo, hi = expense_amounts[cat_idx]
                amount = round(uniform(lo, hi), 2)
                day = randint(1, 28)  # Use 1-28 to avoid month boundary issues
                try:
                    expense_date = datetime(year, month, day).date()
                except ValueError:
                    expense_date = datetime(year, month, 28).date()
                exp = Expense(
                    user_id=user.user_id,
                    category_id=categories[cat_idx].category_id,
                    amount=amount,
                    expense_date=expense_date,
                    description=choice(descriptions)
                )
                db.session.add(exp)
        db.session.commit()
        print("Created sample expenses")

        # Create income
        for month_offset in range(3):
            base_date = now - timedelta(days=30 * month_offset)
            income_date = datetime(base_date.year, base_date.month, 1).date()
            inc = Income(
                user_id=user.user_id,
                amount=round(uniform(25000, 45000), 2),
                income_date=income_date,
                source='Salary'
            )
            db.session.add(inc)
        db.session.commit()
        print("Created sample income")

        # Create budget for current month
        budget = Budget(
            user_id=user.user_id,
            month=now.month,
            year=now.year,
            amount=35000
        )
        db.session.add(budget)
        db.session.commit()
        print("Created sample budget")

        print("\nSeed completed! Login with: demo@expensetracker.com / demo123")

if __name__ == '__main__':
    seed_data()
