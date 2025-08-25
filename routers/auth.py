from typing import Annotated
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from fastapi.security import OAuth2PasswordRequestForm

# app = FastAPI()
router = APIRouter()

# auth.py file is just a route and not the entire application

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    fName: str
    lName: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_pass):
        return False
    return True


# @app.get("/auth")
# @router.get("/auth")
# async def get_user():
#     return {"user": "authenticated"}


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        fname=create_user_request.fName,
        lname=create_user_request.lName,
        role=create_user_request.role,
        hashed_pass=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    # return create_user_model
    db.add(create_user_model)
    db.commit()


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return "Failed Authentication"
    return f"{form_data.username} logged in"  # trudy: i love cats
