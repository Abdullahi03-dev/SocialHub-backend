from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
import shutil, os, uuid
from pathlib import Path
from ..database import get_db
from ..models import User, Post as PostModel
from ..schemas import PostWithUsers as PostSchema

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


#Upload post
@router.post("/upload", response_model=PostSchema)
async def upload_post(
    email: str = Form(...),
    content: str = Form(...),
    tags: str = Form(""),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    # Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check optional image
    file_path = None
    if image:
        allowed_extensions = ["jpg", "jpeg", "png"]
        ext = image.filename.split(".")[-1].lower()
        if ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="Invalid image type. Only JPG/PNG allowed")

        filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR,filename).replace('\\','/')
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    #  Create post
    new_post = PostModel(
        content=content,
        hashtags=tags,
        image=file_path,
        likes=0,
        user_id=user.id
    )

    db.add(new_post)
    # update user post count
    user.posts += 1
    db.commit()
    db.refresh(new_post)

    return new_post


# Get all posts with user info
@router.get("/getallposts", response_model=List[PostSchema])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    if not posts:
        raise HTTPException(status_code=404, detail="User not found")
    return posts




@router.get("/getallpostsForUser/{id}", response_model=List[PostSchema])
def get_posts(id:int,db: Session = Depends(get_db)):
    posts = db.query(PostModel).filter(PostModel.user_id==id).all()
    if not posts:
        raise HTTPException(status_code=404, detail="Posts not found")
    return posts