from models import Base
from db import engine

# Drops all existing tables and recreates them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("✅ Database has been reset.")
