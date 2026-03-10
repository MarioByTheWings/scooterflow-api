from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# En Docker se usa la variable de entorno. Localmente (tests) cae al SQLite de fallback.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# SQLite necesita check_same_thread=False; PostgreSQL no lo admite.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()