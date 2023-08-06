from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_engine(database_url):
    return create_engine(database_url, connect_args={"check_same_thread": False})

def get_sessionmaker(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
