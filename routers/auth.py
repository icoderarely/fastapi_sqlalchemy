from fastapi import APIRouter

# app = FastAPI()
router = APIRouter()

# auth.py file is just a route and not the entire application


# @app.get("/auth")
@router.get("/auth")
async def get_user():
    return {"user": "authenticated"}
