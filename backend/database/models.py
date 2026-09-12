from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from database.session import Base


class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Password login (original MVP) — nullable so Google-only accounts don't
    # need a password.
    username = Column(String, unique=True, index=True)
    password_salt = Column(String)
    password_hash = Column(String)

    # Google Sign-In. `email` is the authorization key: an employee's email
    # must already be present here (provisioned via AUTHORIZED_EMPLOYEE_EMAILS,
    # see auth/seed.py) before their Google account is trusted — signing in
    # with Google never creates a new Staff row on its own. `google_sub` is
    # bound to the account on first successful sign-in and checked on every
    # subsequent one, so a future token for the same email but a different
    # Google account (e.g. after an email is reassigned) is rejected rather
    # than silently accepted.
    email = Column(String, unique=True, index=True, nullable=True)
    google_sub = Column(String, unique=True, index=True, nullable=True)

    display_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class Turn(Base):
    """One line of a customer<->assistant conversation. Doubles as the audit log."""

    __tablename__ = "turns"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String, index=True)
    role = Column(String)  # "customer" or "assistant"
    language = Column(String)
    text_local = Column(Text)
    text_english = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
