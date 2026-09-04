from database import Base, engine
from models import User, Task, FinancialTransaction, JournalEntry  # noqa: F401


def init_database():
    Base.metadata.create_all(bind=engine)
    print("DATABASE TABLES CREATED SUCCESSFULLY")


if __name__ == "__main__":
    init_database()