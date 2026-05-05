import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# DB path is overridable for production (e.g. DB_PATH=/app/data/recipes.db on Fly volume)
DB_PATH = os.getenv("DB_PATH", "./recipes.db")

# Ensure parent dir exists when DB_PATH points into a sub-directory
_db_dir = os.path.dirname(DB_PATH)
if _db_dir:
    os.makedirs(_db_dir, exist_ok=True)

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create the engine (check_same_thread is only needed for SQLite)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Create a session factory (this is how we talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. The base class for our database models
Base = declarative_base()

# 5. Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()