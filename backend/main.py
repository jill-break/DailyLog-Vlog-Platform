from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware 
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI()

# Allow the Frontend to talk to the Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Data Models (Pydantic) ---
class Post(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    video_url: str
    created_at: Optional[str] = None
    likes: int = 0

# --- In-Memory Database (Temporary for Sprint 1 Skeleton) ---
posts_db: List[Post] = []

# --- Routes ---

@app.get("/")
def read_root():
    return {"message": "DailyLog API is healthy"}

@app.get("/posts", response_model=List[Post])
def get_posts():
    # Return posts in reverse chronological order (Newest first)
    return sorted(posts_db, key=lambda x: x.created_at or "", reverse=True)

@app.post("/posts", status_code=201, response_model=Post)
def create_post(post: Post):
    # Generate ID and Timestamp
    post.id = str(uuid.uuid4())
    post.created_at = datetime.utcnow().isoformat()
    
    # Save to "DB"
    posts_db.append(post)
    return post

@app.get("/posts/{post_id}", response_model=Post)
def get_post_detail(post_id: str):
    for post in posts_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=404, detail="Post not found")