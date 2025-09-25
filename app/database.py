from sqlalchemy import create_engine,URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

url = URL.create(
    drivername="postgresql+psycopg2",
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    username=settings.DB_USERNAME,
    password=settings.DB_PASSWORD,
    database=settings.DB_NAME
)

engine = create_engine(url)
Base = declarative_base()
LocalSession = sessionmaker(engine)

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()