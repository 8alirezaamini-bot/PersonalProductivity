from sqlalchemy import select
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash

from models import User


def hash_password(password: str) -> str:
    """Create a secure hash from a plain-text password."""
    return generate_password_hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Check a plain-text password against its stored hash."""
    return check_password_hash(password_hash, password)


def create_user(
    session: Session,
    username: str,
    password: str,
    full_name: str | None = None,
) -> User | None:
    """Create a new user. Return None if the username already exists."""

    existing_user = session.scalar(
        select(User).where(User.username == username)
    )

    if existing_user is not None:
        return None

    user = User(
        username=username,
        password_hash=hash_password(password),
        full_name=full_name,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def authenticate_user(
    session: Session,
    username: str,
    password: str,
) -> User | None:
    """Authenticate a user and return the User object if successful."""

    user = session.scalar(
        select(User).where(User.username == username)
    )

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user