from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .. import models, database

SECRET_KEY = "supersecret"   # move to .env later
ALGORITHM = "HS256"

def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    try:
        # Get token from cookie
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated")

        # Decode JWT
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        # If your IDs are stored as string, don’t force int
        try:
            user_id = int(user_id)  # 🔹 remove this if your ID column is String
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject")

        # Query the DB
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except HTTPException as e:
        # Re-raise known errors
        raise e
    except Exception as e:
        # Log unexpected errors (optional: print/log for debugging)
        print("Unexpected error in get_current_user:", str(e))
        raise HTTPException(status_code=401, detail="Authentication failed")
