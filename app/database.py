from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# postgresql://USERNAME:PASSWORD@HOST/DB_NAME
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi_social_media'

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