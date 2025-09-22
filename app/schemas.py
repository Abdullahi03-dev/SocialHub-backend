# from pydantic import BaseModel, EmailStr
# # import enum
# # from typing import  List
# from typing import Optional
# from datetime import datetime


# # ---------- USER ----------
# class UserCreate(BaseModel):
#     name: str
#     email: str
#     password: str
#     # role:str
    
    

    
    
    
# class UserOut(BaseModel):
#     id: int
#     mame: str
#     email: str
#     role:str
#     posts:int
#     created_at: datetime

#     model_config={
#         "from-attributes": True
# }
    
    
# class PostBase(BaseModel):
#     content: str
#     likes:int
#     tags: Optional[str] = None

# class PostCreate(PostBase):
#     image: Optional[str] = None
#     email: str   # frontend sends email

# class Post(PostBase):
#     id: int
#     image: Optional[str] = None
#     created_at: datetime
#     user_id: int

#     model_config={
#         "from-attributes": True
# }
    
    
from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    # role:str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserBase(BaseModel):
    name: str
    email: str

class UserOut(UserBase):
    id: int
    name:str
    role:str

    model_config={
        "from-attributes": True
}


class Profile(BaseModel):
    id:int
    name:str
    email:EmailStr
    bio:str
    image:str
    location:str
    posts:int
    role:str
    created_at:datetime
    
    model_config={
        "from-attributes": True
}

class idRequest(BaseModel):
    id:int


# Post Schemas
class PostBase(BaseModel):
    content: str
    hashtags: Optional[str] = None

class PostCreate(PostBase):
    email: str  
    # frontend will send email to link post

class Post(PostBase):
    id: int
    image: Optional[str] = None
    likes: int
    created_at: datetime
    # user: UserOut   
    #  nested user info
    
    
class PostWithUsers(PostBase):
    id: int
    image: Optional[str] = None
    likes: int
    created_at: datetime
    user: UserOut   
    model_config={
        "from-attributes": True
}