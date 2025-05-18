from sqlalchemy import create_engine  # Import for creating the database engine
from sqlalchemy.orm import sessionmaker  # Import for session factory

# Database URL for SQLite (can be changed for other DBs)
SQLALCHEMY_DATABASE_URL = "sqlite:///./ecommerce.db"  # or your DB URL

# Create a new SQLite database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
