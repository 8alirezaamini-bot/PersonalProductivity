from database import SessionLocal
from auth import create_user


def main():
    session = SessionLocal()

    try:
        user = create_user(
            session=session,
            username="admin",
            password="Admin1234!",
            full_name="Administrator",
        )

        if user is None:
            print("USER ALREADY EXISTS")
        else:
            print(f"USER CREATED: {user.username}")

    finally:
        session.close()


if __name__ == "__main__":
    main()