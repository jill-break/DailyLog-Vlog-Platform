import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

# --- SQLAlchemy Imports (The Real DB Tools) ---
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# --- 1. Database Setup ---
# Get the URL from docker-compose environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/vlog_db")

# Create the connection engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our SQL tables
Base = declarative_base()

# --- 2. Database Models (SQL Tables) ---
class PostDB(Base):
    __tablename__ = "posts"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    video_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)

# Create the tables in the database (Run migration)
Base.metadata.create_all(bind=engine)

# --- 3. Pydantic Models (Data Validation) ---
# Used for receiving data from the user
class PostCreate(BaseModel):
    title: str
    content: str
    video_url: str

# Used for returning data to the user
class PostResponse(PostCreate):
    id: str
    created_at: datetime
    likes: int

    class Config:
        orm_mode = True # Tells Pydantic to read from SQLAlchemy objects

# --- 4. Dependencies ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 5. CORS Middleware (Security) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 6. API Endpoints ---

@app.get("/health")
def health_check():
    """Monitoring endpoint for Sprint 2"""
    return {"status": "healthy", "database": "connected"}

@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # Fetch from real DB, sorted by date
    return db.query(PostDB).order_by(PostDB.created_at.desc()).all()

@app.post("/posts", status_code=201, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Create SQL Object
    db_post = PostDB(
        id=str(uuid.uuid4()),
        title=post.title,
        content=post.content,
        video_url=post.video_url,
        created_at=datetime.utcnow()
    )
    # Add and Commit
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post_detail(post_id: str, db: Session = Depends(get_db)):
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post