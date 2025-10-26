from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
from app.core.config import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt

from app.database import SessionLocal
from app.models.user import User

def get_db():
    db = SessionLocal()
    try:
       yield db
    finally:
        db.close()
db_dependency = Annotated[Session, Depends(get_db)]

def get_current_user(token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db) ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

user_dependency = Annotated[dict, Depends(get_current_user)]

