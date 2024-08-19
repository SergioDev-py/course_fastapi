from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


"""
Documentation for engine cofiguration (SQLAlchemy): https://docs.sqlalchemy.org/en/20/core/engines.html

basic postgresql URL: postgresql://<username>:<password>@<ip-address/hostname>:<port>/<database_name>
"""
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try: 
        yield db
    except:
        db.close()
        raise # So freaking important when working with sqlAlchemy or sqlmodel