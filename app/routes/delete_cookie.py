# from fastapi import Response,APIRouter
# router = APIRouter()

# @router.post("/logout")

# # HOW TO DELETE COOKIE SAVED DURING AUTH FOR LOGGGING OUT
# def logout(response: Response):
#     response.delete_cookie(
#         key="access_token",
#         httponly=True,
#         samesite="none",
#         secure=True,
#         ) 
#     return {"message": "Logged out"}



from fastapi import Response, APIRouter

router = APIRouter()

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        samesite="none",
        secure=True,   # must match how you originally set the cookie
        path="/",      # include this so deletion works across your API routes
        domain="https://socialhub-backend-se80.onrender.com"  # must match the domain used in set_cookie
    )
    return {"message": "Logged out"}
