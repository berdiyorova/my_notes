from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DB_USER, DB_PASS, DB_HOST, DB_NAME

# PostgreSQL bazasiga ulanish uchun URL
#                         "postgresql://username:password@localhost/db_name"
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

# Engine yaratish
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessiya yaratish
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base yaratish
Base = declarative_base()

# Sessiya ochish
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
