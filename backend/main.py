import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
import logging

# --- SQLAlchemy Imports ---
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

app = FastAPI()

# ---  Configure Logging (Console + File) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"), # <--- Writes to a file named 'app.log'
        logging.StreamHandler()         # <--- Writes to the terminal
    ]
)
logger = logging.getLogger(__name__)

# --- Database Setup ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/vlog_db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Models (SQL Tables) ---
class CommentDB(Base):
    __tablename__ = "comments"
    id = Column(String, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    post_id = Column(String, ForeignKey("posts.id")) # Link to Post

    # Relationship back to Post
    post = relationship("PostDB", back_populates="comments")

class PostDB(Base):
    __tablename__ = "posts"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    video_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)
    
    # Relationship to Comments
    comments = relationship("CommentDB", back_populates="post", cascade="all, delete-orphan")

# Create Tables
Base.metadata.create_all(bind=engine)

# --- Pydantic Models (Data Validation) ---

# Model for creating a comment
class CommentCreate(BaseModel):
    content: str

# Model for displaying a comment
class CommentResponse(BaseModel):
    id: str
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str
    video_url: str

# Updated Post Response (includes list of comments)
class PostResponse(PostCreate):
    id: str
    created_at: datetime
    likes: int
    comments: List[CommentResponse] = [] # Nested comments

    class Config:
        orm_mode = True

# --- Dependencies ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints ---

@app.get("/health")
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested")
    return {"status": "healthy", "database": "connected"}
# --- Get Posts Endpoint (US-2) ---
@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    """Retrieve all vlog posts"""
    logger.info("Fetching all posts")
    return db.query(PostDB).order_by(PostDB.created_at.desc()).all()
#--- Create Post Endpoint (US-1) ---
@app.post("/posts", status_code=201, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    """Create a new vlog post"""
    db_post = PostDB(
        id=str(uuid.uuid4()),
        title=post.title,
        content=post.content,
        video_url=post.video_url,
        created_at=datetime.utcnow()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    logger.info(f"Created new post with ID: {db_post.id}")
    return db_post
# --- Like Post Endpoint (US-4) ---
@app.post("/posts/{post_id}/like", response_model=PostResponse)
def like_post(post_id: str, db: Session = Depends(get_db)):
    """Like a vlog post"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes += 1 # type: ignore
    db.commit()
    db.refresh(post)
    logger.info(f"Post {post_id} liked. Total likes: {post.likes}")
    return post

# --- Comment Endpoint (US-5) ---
@app.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(post_id: str, comment: CommentCreate, db: Session = Depends(get_db)):
    """Create a comment for a specific post"""
    # Check if post exists
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Create comment
    db_comment = CommentDB(
        id=str(uuid.uuid4()),
        content=comment.content,
        post_id=post_id,
        created_at=datetime.utcnow()
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    logger.info(f"Created comment {db_comment.id} for post {post_id}")
    return db_comment
# --- US-3 Get Post Detail Endpoint ---
@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post_detail(post_id: str, db: Session = Depends(get_db)):
    """Retrieve a specific post by ID"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    logger.info(f"Fetching post with ID: {post_id}")
    return post
# --- Delete Post Endpoint (US-6) ---
@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: str, db: Session = Depends(get_db)):
    """Delete a vlog post and its comments"""
    post = db.query(PostDB).filter(PostDB.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(post)
    db.commit()

    logger.info(f"Deleted post with ID: {post_id} and its comments")    
    return None
# --- Delete Comment Endpoint ---
@app.delete("/comments/{comment_id}", status_code=204)
def delete_comment(comment_id: str, db: Session = Depends(get_db)):
    """Delete a specific comment"""
    comment = db.query(CommentDB).filter(CommentDB.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    db.delete(comment)
    db.commit()
    logger.info(f"Deleted comment with ID: {comment_id}")
    return None