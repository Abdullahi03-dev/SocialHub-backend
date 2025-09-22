from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from .. import models, schemas, database

router = APIRouter()

@router.get("/top-users", response_model=list[schemas.UserBase])
def get_top_users(db: Session = Depends(database.get_db)):
    # Step 1: Get unique user_ids from posts
    user_ids = db.query(distinct(models.Post.user_id)).all()
    user_ids = [u[0] for u in user_ids]  # flatten [(1,), (2,), (3,)] → [1,2,3]

    # Step 2: Fetch users with those IDs
    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    
    return users




@router.get("/top-hashtags")
def get_top_hashtags(db: Session = Depends(database.get_db)):
    hashtags = (
        db.query(models.Post.hashtags)   # only fetch hashtags column
        .order_by(models.Post.created_at.desc())
        .limit(5)
        .all()
    )
    # SQLAlchemy returns list of tuples like [("webdev,python",), ("react,js",)...]
    return [h[0] for h in hashtags]