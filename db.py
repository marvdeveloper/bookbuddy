from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create an SQLite database in the local folder called bookbuddy.db
SQLALCHEMY_DATABASE_URL = "sqlite:///bookbuddy.db"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal class will be used to create session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models to inherit
Base = declarative_base()


# Dependency for creating sessions, useful in your CLI or other parts
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
