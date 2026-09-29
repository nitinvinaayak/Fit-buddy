from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


DATABASE_URL = settings.database_url

connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(String(100), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=False)

    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)

    goal = Column(String(100), nullable=False)
    intensity = Column(String(50), nullable=False)

    original_plan = Column(Text, nullable=True)
    updated_plan = Column(Text, nullable=True)

    nutrition_tip = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


def init_db():
    """Create database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Provide a database session."""
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def save_user(db, user: User):
    """Save a new user to the database."""
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db, user_id: str):
    """Find a user using their user ID."""
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def get_all_users(db):
    """Return all users."""
    return (
        db.query(User)
        .order_by(User.created_at.desc())
        .all()
    )


def update_user_plan(
    db,
    user: User,
    updated_plan: str,
    feedback: str | None = None,
):
    """Update a user's workout plan and feedback."""
    user.updated_plan = updated_plan

    if feedback:
        user.feedback = feedback

    db.commit()
    db.refresh(user)

    return user