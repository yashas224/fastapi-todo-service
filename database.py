from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

sqlite = "SQLite"
postgres = "PostgreSQL"
load_dotenv()
SQL_ALCHEMY_DATABASE_URL = ""
engine = None

db_config = os.getenv("DB_CONFIG")
db_password = os.getenv("DB_PASSWORD")
print(f"initializing DB config: {db_config}")

if db_config == sqlite:
    SQL_ALCHEMY_DATABASE_URL = "sqlite:///./todo-service.db"
    engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False, "timeout": 30},
                           echo=True)
elif db_config == postgres:
    SQL_ALCHEMY_DATABASE_URL = f"postgresql://postgres:{db_password}@localhost:5432/TodoApplicationDatabase"
    engine = create_engine(SQL_ALCHEMY_DATABASE_URL,
                           echo=True)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass
