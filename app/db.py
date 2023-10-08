from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, orm
from sqlalchemy.future import Engine

DATABASE_URL = "postgresql://postgres:postgres@localhost/ecommerce_db"
engine: Engine = create_engine(DATABASE_URL, future=True)

SessionLocal = orm.scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True))

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["engine", "SessionLocal", "get_db"]
