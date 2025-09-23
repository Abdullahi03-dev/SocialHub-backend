from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from .. import schemas, models, database
from ..utils.auth import get_current_user


# AUTH ROUTER

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------------------
# PASSWORD HASHING CONFIGURATION ->HOW TO HASH PASSWORS
# -------------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# -------------------------------
# SIGNUP ENDPOINT
# -------------------------------
@router.post('/signup')
async def SignUp(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role='member',
        posts=0,
        created_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"msg": "User created successfully"}


# -------------------------------
# SIMPLE TEST ENDPOINT TO CHECK IF EVERYTHING IS WROKING
# -------------------------------
@router.post('/testing')
def testing():
    print('hello')


# -------------------------------
# JWT CONFIGURATION
# -------------------------------
SECRET_KEY = "supersecret"    
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600   # token validity in minutes


# -------------------------------
# SIGNIN ENDPOINT
# -------------------------------
@router.post("/signin")
def signin(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Set token expiry
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {
        "sub": str(db_user.id),  
        "email": db_user.email,   
        "role": db_user.role,    
        "exp": int(expire.timestamp())
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Attach token to response as cookie
    response = JSONResponse({"msg": "Login successful"})
    # response.set_cookie(
    #     key="access_token",
    #     value=token,
    #     httponly=True,
    #     samesite="none",
    #     secure=True,   # set to True when using HTTPS WHN AM TRYIGN TO HOST
    #     max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,   # cookie duration in seconds
    #     expires=int(expire.timestamp())
    # )
    response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,          # protects from JavaScript access (XSS)
    samesite="none",        # required if frontend + backend are on different domains
    secure=True,            # ensures cookie is sent only over HTTPS
    max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # lifetime in seconds
    expires=int(expire.timestamp()),           # exact expiry
    path="/",               # restricts cookie to your API path
    domain="socialhub-backend-se80.onrender.com" # set this to your backend domain (or leave None on localhost)
)

    return response


# -------------------------------
# FETCH USER BY EMAIL
# 
@router.post('/fetchbyemail', response_model=schemas.Profile)
def get_user_by_email(request: schemas.idRequest, db: Session = Depends(database.get_db)):
    """
    Fetch a user's profile using their email.
    Used when frontend already knows the email.
    """
    user = db.query(models.User).filter(models.User.id == request.id).first()
    if not user:
        raise HTTPException(status_code=404, detail='USER NOT FOUND')
    return user


# -------------------------------
# CHECK AUTH (TOKEN VALIDATION)
# -------------------------------
@router.get("/check-auth")
def check_auth(access_token: str = Cookie(None)):
    # """
    # Check if a user is authenticated.
    # - Looks for JWT in cookies.
    # - Returns True/False depending on validity.
    # """
    if not access_token:
        return {"authenticated": False}
    try:
        jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"authenticated": True}
    except JWTError:
        return {"authenticated": False}


# -------------------------------
# GET CURRENT LOGGED-IN USER
# -------------------------------
@router.get("/", response_model=schemas.Profile)
def me(user = Depends(get_current_user)):
    # Return the profile of the currently authenticated user.
    # Uses the `get_current_user` utility function.
    return user
