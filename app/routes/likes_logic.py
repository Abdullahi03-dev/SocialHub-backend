from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. models import Post, PostLike, User
from .. database import get_db

router = APIRouter()

# Toggle Like/Unlike
# -------------------LIKE LOGIC FOR POSTS----------------------
# ---------
@router.post("/posts/{post_id}/like/{email}")
def toggle_like(post_id: int, email: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_like = (
        db.query(PostLike)
        .filter(PostLike.user_id == user.id, PostLike.post_id == post_id)
        .first()
    )

    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.likes -= 1
        db.commit()
        return {"message": "Unliked", "likes": post.likes}
    else:
        # Like
        new_like = PostLike(user_id=user.id, post_id=post_id)
        db.add(new_like)
        post.likes += 1
        db.commit()
        return {"message": "Liked", "likes": post.likes}
    






@router.get("/getLiked/{post_id}/liked/{email}")
def check_liked(post_id: int, email: str, db: Session = Depends(get_db)):
    # find user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"liked": False} 

    # check if like exists
    existing_like = (
        db.query(PostLike)
        .filter(PostLike.user_id == user.id, PostLike.post_id == post_id)
        .first()
    )

    return {"liked": bool(existing_like)}
    