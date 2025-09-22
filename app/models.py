from sqlalchemy import Column, Integer, String,DateTime,func,Text,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . database import Base

# -------------------------
# User Model
# -------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)
    bio=Column(String)
    location=Column(String)
    posts = Column(Integer, default=0)  # number of posts by user
    role=Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
 
    user_posts = relationship("Post", back_populates="user")
    likes_id = relationship("PostLike", back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    hashtags = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)   # optional
    likes = Column(Integer, default=0)           # likes count
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="user_posts")
    likes_id = relationship("PostLike", back_populates="post")
    
    
class PostLike(Base):
    __tablename__ = "post_likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.email", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="likes_id")
    post = relationship("Post", back_populates="likes_id")
    