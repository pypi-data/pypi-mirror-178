from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from compute_service.api import models

engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)

def override_get_session():
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()
