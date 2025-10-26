from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.config import SECRET_KEY, ALGORITHM

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.util import deprecated
from starlette import status

from app.security import hash_password, verify_password
from app.schemas import UserCreate
from app.database import SessionLocal
from app.dependency import db_dependency, user_dependency
from app.models.user import User
from app.schemas import UserCreate, UserLogin, UserResponse


router = APIRouter(prefix="/user", tags=["user"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#- GET /list → get all users (with pagination).
# POST /createUser → Create new user (already done).
#- GET /getUser/{id} → Read user by ID.
#- PUT /user/{id} → Update user (with unique username/email checks).
# DELETE /deleteUser/{id} → Delete user.



@router.get("/list")
def list_users(skip: int = 0, limit: int = 10, db: db_dependency = None, jwtuser: user_dependency = None):
    if jwtuser is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    users = db.query(User).offset(skip).limit(limit).all()
    return users



@router.post("/create")
def create_user(payload: UserCreate, db: db_dependency,  
                jwtuser: user_dependency ):
    if jwtuser is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered")

    user = User(
        username=payload.username,
        hashed_password=hash_password(payload.password),
        email=payload.email,
        full_name=payload.full_name,
        dob=payload.dob,
        sex = payload.sex,
        height_cm=payload.height_cm,
        weight_kg=payload.weight_kg
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": f"User {user.username} has been created successfully"}
    #return {"id": user.id, "username": user.username, "email": user.email}

@router.get("/get/{user_id}")
def read_user(user_id: int, db: db_dependency, jwtuser: user_dependency):
    if jwtuser is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "dob": user.dob,
        "sex" : user.sex,
        "height_cm": user.height_cm,
        "weight_kg": user.weight_kg,
        "bmi": user.bmi
    }

@router.put("/update")
def update_user(    
    payload: UserCreate,
    db: db_dependency,
    jwtuser: user_dependency ):
    if jwtuser is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Failed")

    user = db.query(User).filter(User.id == payload.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    #  Check for unique username if changed
    if payload.username != user.username:
        if db.query(User).filter(User.username == payload.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = payload.username

    #  Check for unique email if changed
    if payload.email != user.email:
        if db.query(User).filter(User.email == payload.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = payload.email

    # Optional fields
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.dob is not None:
        user.dob = payload.dob
    if payload.sex is not None:
        user.sex = payload.sex
    if payload.password is not None:
        user.hashed_password = hash_password(payload.password)

    db.commit()
    db.refresh(user)

    return {"detail": f"User {user.username} has been updated successfully"}
    """ return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "dob": user.dob
    } """



@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: db_dependency, jwtuser: user_dependency):
    if jwtuser is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": f"User {user.username} deleted successfully"}



