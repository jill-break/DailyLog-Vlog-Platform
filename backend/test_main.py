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
# Used a separate in-memory database for the actual tests to keep them clean.
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


# Test Case 1
def test_read_health():
    """Check if the health endpoint works"""
    response = client.get("/health")
    assert response.status_code == 200
   
    assert response.json()["status"] == "healthy"

# Test Case 2
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

# Test Case 3
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

# Test Case 4
def test_delete_post():
    """Test deleting a post (US-6)"""
    # 1. Create a post to delete
    payload = {
        "title": "Post to Delete",
        "content": "This will be gone soon",
        "video_url": "http://delete.me"
    }
    create_res = client.post("/posts", json=payload)
    post_id = create_res.json()["id"]
    
    # 2. Delete the post
    delete_res = client.delete(f"/posts/{post_id}")
    assert delete_res.status_code == 204 # 204 means "Success, No Content"
    
    # 3. Verify it is gone
    get_res = client.get(f"/posts/{post_id}")
    assert get_res.status_code == 404

# Test Case 5
def test_delete_post_cascade():
    """Test that deleting a post also deletes its comments"""
    # 1. Create Post
    post_res = client.post("/posts", json={"title": "Cascade Test", "content": "...", "video_url": "..."})
    post_id = post_res.json()["id"]
    
    # 2. Add Comment
    comment_res = client.post(f"/posts/{post_id}/comments", json={"content": "I should be deleted too"})
    comment_id = comment_res.json()["id"]
    
    # 3. Delete Post
    client.delete(f"/posts/{post_id}")
    # 4. Verify Comment is Deleted
    del_comment_res = client.delete(f"/comments/{comment_id}")
    assert del_comment_res.status_code == 404