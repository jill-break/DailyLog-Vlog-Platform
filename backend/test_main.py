import os

# --- CRITICAL FIX ---
# Set the DATABASE_URL to use SQLite (in-memory) BEFORE importing main.
# This prevents main.py from trying to connect to the real Postgres DB and crashing.
os.environ["DATABASE_URL"] = "sqlite:///./test_temp.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_db, Base

# --- 1. Setup Test Database ---
# We use a separate in-memory database for the actual tests to keep them clean.
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the test database
Base.metadata.create_all(bind=engine)

# --- 2. Override the Dependency ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# --- 3. The Tests ---

def test_read_health():
    """Check if the health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
    # Note: The status might vary depending on main.py logic, but we expect success
    assert response.json()["status"] == "healthy"

def test_create_post():
    """Test creating a new vlog post (US-1)"""
    payload = {
        "title": "My Docker Vlog",
        "content": "Running on Postgres now!",
        "video_url": "http://youtube.com/docker"
    }
    response = client.post("/posts", json=payload)
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Docker Vlog"
    assert "id" in data
    assert data["likes"] == 0

def test_get_posts():
    """Test retrieving the list of posts (US-2)"""
    # Create a post first so we have something to fetch
    client.post("/posts", json={
        "title": "Test Post",
        "content": "Content",
        "video_url": "url"
    })
    
    response = client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1