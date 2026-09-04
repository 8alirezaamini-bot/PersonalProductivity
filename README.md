# Personal Productivity

A web-based personal productivity management system developed with Python and Streamlit.

## Overview

Personal Productivity is a web application designed to help users manage their daily activities, tasks, finances, and personal journal entries in one place.

The application provides a simple dashboard where users can track their productivity and manage their personal information securely.

## Features

- User authentication and login system
- Secure password hashing
- Personal dashboard
- Task management
  - Create tasks
  - Edit tasks
  - Delete tasks
  - Complete and reopen tasks
  - Filter tasks by priority and status
  - Set due dates
- Financial management
  - Add income and expenses
  - View current balance
  - View transaction history
  - Delete transactions
- Personal journal
  - Create journal entries
  - Edit entries
  - Delete entries
  - Browse entries by date
  - Monthly calendar view
- User settings
  - Change full name
  - Change password
  - Logout
- User-specific data isolation
- MySQL database integration
- SQLAlchemy ORM

## Technologies

- Python 3.11
- Streamlit
- SQLAlchemy
- MySQL
- PyMySQL
- Werkzeug
- python-dotenv
- HTML/CSS


Installation
1. Clone the repository
git clone https://github.com/8alirezaamini-bot/PersonalProductivity.git
cd PersonalProductivity
2. Create a virtual environment
python -m venv .venv
3. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
4. Install dependencies
pip install -r requirements.txt
Database Setup

The application uses MySQL as its database.

Create a MySQL database and configure the database connection using environment variables.

Create a .env file in the project root:

DB_HOST=localhost
DB_PORT=3306
DB_NAME=personal_productivity
DB_USER=your_username
DB_PASSWORD=your_password

Do not commit the .env file to GitHub.

Initialize the Database

Run:

python init_db.py

To create a user:

python create_user.py
Running the Application

Start the Streamlit application with:

streamlit run app.py

The application will open in your browser.
Security

The application uses password hashing for storing user passwords.

Sensitive configuration data such as database credentials is stored in environment variables and should not be committed to the repository.

Future Improvements

Possible future improvements include:

Email notifications
Task reminders
Data visualization and statistics
Exporting financial data
Improved mobile responsiveness
Cloud deployment
Backup and restore functionality
Author

Alireza Amini
