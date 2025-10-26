# app/schemas.py
from pydantic import BaseModel, constr, validator
from datetime import date
from typing import Optional


class UserCreate(BaseModel):
   # id: int
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=8,  max_length=20)
    full_name: constr(max_length=30)
    email: constr(max_length=30)
    sex: str
    dob: date  # 'yyyy-mm-dd' format
    height_cm : Optional[float]   # height in centimeters
    weight_kg : Optional[float]    # weight in kilograms




class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
"""
@validator("bmi", always=True)
def calculate_bmi(cls, v, values):
    height_cm = values.get("height_cm")
    weight_kg = values.get("weight_kg")
    if height_cm and weight_kg:
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 2)
    return None """

