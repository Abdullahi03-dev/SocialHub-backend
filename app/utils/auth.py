from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from .. import models, database

SECRET_KEY = "supersecret"   # move to .env later
ALGORITHM = "HS256"

def get_current_user(request: Request, db: Session = Depends(database.get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        # force cast to int safely
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            raise HTTPException(status_code=401, detail="Invalid token subject")
        # query the DB
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception:
        # catch any unexpected error → don’t let it crash as 500
        raise HTTPException(status_code=401, detail="Authentication failed")
