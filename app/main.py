from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import auth,fetchUsers,add_post,delete_cookie,analytics_fetch,edit_user,likes_logic,checkAdmin # your routers

app = FastAPI()

# Allow your frontend origin
origins = [
    "https://socialhub.pxxl.xyz"
    "http://localhost:5173",  
    "http://localhost:3000",  
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
# Routers
app.include_router(auth.router)
app.include_router(fetchUsers.router)
app.include_router(add_post.router)
app.include_router(delete_cookie.router)
app.include_router(analytics_fetch.router)
app.include_router(edit_user.router)
app.include_router(likes_logic.router)
app.include_router(checkAdmin.router)