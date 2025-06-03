from bookbuddy.models import Base
from bookbuddy.db import engine

def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Database has been reset.")

if __name__ == "__main__":
    reset_database()
