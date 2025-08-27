from datetime import timedelta, timezone, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt

# app = FastAPI()
router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "cff43c7e90ffd38c70126a9189fce56010d652d3da158f2b8302499afc191c4e"
ALGORITHM = "HS256"

# auth.py file is just a route and not the entire application

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    email: str
    fName: str
    lName: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


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
        return None
    if not bcrypt_context.verify(password, user.hashed_pass):
        return None
    return user


# @app.get("/auth")
# @router.get("/auth")
# async def get_user():
#     return {"user": "authenticated"}


@router.post("/", status_code=status.HTTP_201_CREATED)
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


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # username: str = payload.get("sub")
        username = payload.get("sub")
        # user_id: int = payload.get("id")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate user",
            )
        username = str(username)
        user_id = int(user_id)
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate user"
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        # return "Failed Authentication"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="could not validate user",
        )

    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    # return f"{form_data.username} logged in with token {token}"  # trudy: i love cats
    return {"access_token": token, "token_type": "bearer"}
