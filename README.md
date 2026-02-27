# Expense Tracker with Financial Insights

A secure web application for tracking expenses and income, visualizing spending patterns, and receiving automated financial insights. Built as a BCA Final Year Project.

## Features

- **User Authentication**: Register, login, logout with hashed passwords and session management
- **Expense Management**: Add, edit, delete expenses with category assignment
- **Income Management**: Track income sources and dates
- **Categories**: Create custom expense categories
- **Budgets**: Set monthly budgets and get overspending alerts
- **Dashboard**: Total income, expense, savings cards; category pie chart; monthly trend line chart
- **Financial Insights**: Savings %, month-over-month comparison, budget exceeded alerts, highest spending category
- **Reports**: Download PDF report and export to Excel

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap 5
- **Database**: SQLite
- **Charts**: Chart.js
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## Project Structure

```
expense_tracker/
├── app/
│   ├── __init__.py          # App factory, extensions
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── category.py
│   │   ├── expense.py
│   │   ├── income.py
│   │   └── budget.py
│   ├── routes/              # Blueprint routes
│   │   ├── auth.py
│   │   ├── main.py
│   │   ├── expenses.py
│   │   ├── income.py
│   │   ├── categories.py
│   │   ├── budgets.py
│   │   └── reports.py
│   └── templates/           # Jinja2 HTML templates
├── scripts/
│   └── seed_data.py         # Sample data seeder
├── config.py
├── run.py
└── requirements.txt
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 2. Create Virtual Environment (Recommended)

```bash
cd expense_tracker
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python run.py
```

The app will start at `http://127.0.0.1:5000`

### 5. Seed Sample Data (Optional)

```bash
python -m scripts.seed_data
```

This creates a demo user:
- **Email**: demo@expensetracker.com
- **Password**: demo123

## Database

- SQLite database file: `expense_tracker.db` (created automatically on first run)
- For MySQL: Set `DATABASE_URL` environment variable to your MySQL connection string

## Viva / Interview Points

1. **MVC Architecture**: Models (SQLAlchemy), Views (Jinja2 templates), Controllers (Flask routes/blueprints)
2. **Security**: Password hashing (Werkzeug pbkdf2:sha256), `@login_required`, form validation
3. **Data Isolation**: Each user sees only their own data via `user_id` filters
4. **ORM Benefits**: SQLAlchemy handles SQL, migrations, relationships
5. **Financial Insights Logic**: Savings %, month-over-month comparison, budget alerts, category analysis
6. **Scalability**: Blueprint modular structure, ready for AI/ML features (e.g., expense prediction)

## Deploy on Render

### Option 1: Using Dashboard (Recommended)

1. **Push your code to GitHub** (create a repo and push the project).

2. **Sign up at [render.com](https://render.com)** and connect your GitHub account.

3. **Create a new Web Service**:
   - Click **New +** → **Web Service**
   - Connect your GitHub repo (`expense_tracker`)
   - Select the repo and click **Connect**

4. **Configure the service**:
   | Field | Value |
   |-------|-------|
   | Name | expense-tracker (or any name) |
   | Region | Oregon (US West) or nearest |
   | Runtime | Python 3 |
   | Build Command | `pip install -r requirements.txt` |
   | Start Command | `gunicorn wsgi:app --bind 0.0.0.0:$PORT` |
   | Instance Type | Free |

5. **Environment Variables** (in Render Dashboard → Environment):
   | Key | Value |
   |----|-------|
   | `SECRET_KEY` | Generate a random string (or use Render's "Generate" button) |
   | `FLASK_ENV` | `production` |

6. **Deploy** – Click **Create Web Service**. Render will build and deploy. Your app will be live at `https://your-app-name.onrender.com`.

### Option 2: Using render.yaml (Blueprint)

If you have `render.yaml` in your repo:

1. Push code to GitHub.
2. In Render Dashboard → **New +** → **Blueprint**.
3. Connect the repo – Render will detect `render.yaml` and create the service.
4. Add `SECRET_KEY` in Environment variables (Blueprint auto-generates it if configured).

### Notes for Render

- **Free tier**: App sleeps after 15 minutes of inactivity; first request may take ~30 seconds to wake.
- **SQLite**: Works on Render, but data resets on redeploy. For persistent data, use [Render PostgreSQL](https://render.com/docs/databases) and set `DATABASE_URL`.
- **Port**: Render sets `PORT` automatically; Gunicorn uses it by default.

## Environment Variables (Production)

```bash
export SECRET_KEY="your-secure-random-key"
export DATABASE_URL="sqlite:///path/to/db.db"  # or MySQL URL
export FLASK_ENV="production"
```

## License

Educational use - BCA Project.
