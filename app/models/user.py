from app.database import Base
from pydantic import BaseModel
from typing import Annotated
from sqlalchemy import Column, Integer, String,  Float, ForeignKey, Date

import re

DateStr = Annotated[str, re.compile(r"^\d{4}-\d{2}-\d{2}$")]



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    sex = Column(String, nullable=True)
    dob = Column(Date, nullable=True)  # date of birth  'yyyy-mm-dd'
    height_cm = Column(Float, nullable=True)  # height in centimeters
    weight_kg = Column(Float, nullable=True)  # weight in kilograms    
    bmi = Column(Float, nullable=True)  # Body Mass Index

    def calculate_bmi(self) -> float | None:
        """Return BMI if height and weight are set, else None."""
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m ** 2), 2)
        return None


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    dob: DateStr
    sex: str
    height_cm: float
    weight_kg: float
    bmi: float

    # JWT fields
    #access_token: str
    #token_type: str = "bearer"

class Config:
    orm_mode = True

class UserWithToken(BaseModel):
    user: UserOut
    access_token: str
    token_type: str = "bearer"
    detail: str



