
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db
from app.models.article import Article
from app.models.source import Source
from app.models.category import Category

SQLALCHEMY_TEST_URL = 'sqlite://'
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
from sqlalchemy import inspect
print(inspect(engine).get_table_names())
client = TestClient(app)
r = client.get('/api/v1/articles/')
print(r.status_code)

