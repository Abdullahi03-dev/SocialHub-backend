from fastapi import Response,APIRouter
router = APIRouter()

@router.post("/logout")

# HOW TO DELETE COOKIE SAVED DURING AUTH FOR LOGGGING OUT
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True,
        ) 
    return {"message": "Logged out"}