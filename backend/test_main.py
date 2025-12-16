from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Check if the API is alive"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "DailyLog API is healthy"}

def test_create_post():
    """Test creating a new vlog post (US-1)"""
    payload = {
        "title": "My First Vlog",
        "content": "Today I learned FastAPI",
        "video_url": "http://youtube.com/fake"
    }
    response = client.post("/posts", json=payload)
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My First Vlog"
    assert "id" in data
    assert "created_at" in data

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
    assert len(response.json()) > 0