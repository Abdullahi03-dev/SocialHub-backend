from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
# import random, string
from .. database import get_db
from .. import models
# from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

# _____________________------------------------
# THIS IS USED FOR FETCHING USERS ALL USERS 
# -------------------------------------
@router.get('/')
def fetch_user(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=404, detail="NO DATE GOTTEN")
    return users


@router.get('/membersLength')
def fetch_members_length(db:Session=Depends(get_db)):
    members_length=db.query(models.User).filter(models.User=='member').count()
    admin_length=db.query(models.User).filter(models.User=='admin').count()
    
    return {
        'members':members_length,
        'admins':admin_length
    }
    
    