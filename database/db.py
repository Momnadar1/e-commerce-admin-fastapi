from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

host = "localhost"
user = "root"
password = "root"
database_name = "walmart"
port = 3306

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
