from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# postgresql://USERNAME:PASSWORD@HOST/DB_NAME
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all models will expend this class
Base = declarative_base()

# establish connection
# will be sed in all route/path calls 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()