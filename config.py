import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "personal_productivity")
DB_USER = os.getenv("DB_USER", "pp_app")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")