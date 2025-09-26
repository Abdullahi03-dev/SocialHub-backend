from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from .. import models,  database



router=APIRouter(prefix='/checkAdmin')

@router.get('/{savedEmail}')
def check_Admin(savedEmail:str,db:Session=Depends(database.get_db)):
    user=db.query(models.User).filter(models.User.email==savedEmail).first()
    if not user:
        raise HTTPException(status_code=404,detail='USER NOT FOUND')
    return {'is_admin':user.role.lower()=='admin'}