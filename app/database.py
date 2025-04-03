from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings as ss

SQLALCHEMY_DATABASE_URL = f"postgresql://{ss.db_username}:{ss.db_password}@{ss.db_hostname}:{ss.db_port}/{ss.db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
