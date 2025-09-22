from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
import shutil, os, uuid
from .. import models, database


# -------------------------------
# EDIT ROUTER
# -------------------------------
# Handles updating user info and uploading images
router = APIRouter(prefix='/edit', tags=['Edit'])


# -------------------------------
# SCHEMA FOR USER UPDATE
# -------------------------------
class UserUpdate(BaseModel):
    name: str
    bio: str
    location: str


# -------------------------------
# UPDATE USER INFO
# -------------------------------
@router.put("/editUser/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.bio = user.bio
    db_user.location = user.location

    db.commit()
    db.refresh(db_user)

    return {"message": "User updated successfully", "user": db_user}



UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  







# ALREADY A DEFAULT IMAGE BUT IF YOU WISH TO EDIT YOU CAN->
# UPLOAD USER PROFILE IMAGE
# -------------------------------
@router.put("/editImage/{email}/upload-image")
async def upload_image(email: str, file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    # """
    # Upload and update a user's profile image.
    # - Validates file type (must be image).
    # - Saves file locally in 'uploads' directory.
    # - Updates user's image path in the database.
    # """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images allowed.")

    # Create file path (normalize slashes for cross-platform use)
    file_path = os.path.join(UPLOAD_DIR, file.filename).replace('\\', '/')

    # Save file to local storage
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update user's image path in database
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.image = file_path
    db.commit()
    db.refresh(user)

    return {"message": "Image uploaded successfully", "path": user.image}
