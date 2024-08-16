from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date
from app.models.gender import Gender
from typing import Optional
import re

class BasicInfoCreate(BaseModel):
    name: str 
    gender: Gender
    birthdate: date

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('Name must have at least 3 characters.')
        if len(v) > 128:
            raise ValueError('Name cannot exceed 128 characters.')
        return v

    @field_validator('birthdate')
    def validate_birthdate(cls, v):
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v.strftime('%Y-%m-%d')):
            raise ValueError('Birthdate must be in the format yyyy-mm-dd.')
        return v
    

class BasicInfoUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[Gender] = None
    birthdate: Optional[date] = None

    @field_validator('name')
    def validate_name(cls, v):
        if len(v) < 3:
            raise ValueError('Name must have at least 3 characters.')
        if len(v) > 128:
            raise ValueError('Name cannot exceed 128 characters.')
        return v

    @field_validator('birthdate')
    def validate_birthdate(cls, v):
        if v is not None:
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', v.strftime('%Y-%m-%d')):
                raise ValueError('Birthdate must be in the format yyyy-mm-dd.')
        return v

class BasicInfoResponse(BaseModel):
    id: int
    name: str
    gender: str
    birthdate: date

    model_config = ConfigDict(from_attributes=True)


class DoctorEmployeeCreate(BasicInfoCreate):
    username: str
    password: str

    @field_validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must have at least 3 characters.')
        if len(v) > 32:
            raise ValueError('Username cannot exceed 32 characters.')
        if not re.match("^[a-zA-Z0-9_-]+$", v):
            raise ValueError('Username can only contain letters, numbers, underscores, and hyphens.')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8 or len(v) > 32:
            raise ValueError('Password must be between 8 and 32 characters long.')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number.')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character.')
        return v

class DoctorEmployeeUpdate(BasicInfoUpdate):
    username: Optional[str] = None
    password: Optional[str] = None

    @field_validator('username')
    def validate_username(cls, v):
        if v is not None:
            if len(v) < 3:
                raise ValueError('Username must have at least 3 characters.')
            if len(v) > 32:
                raise ValueError('Username cannot exceed 32 characters.')
            if not re.match("^[a-zA-Z0-9_-]+$", v):
                raise ValueError('Username can only contain letters, numbers, underscores, and hyphens.')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if v is not None:
            if len(v) < 8 or len(v) > 32:
                raise ValueError('Password must be between 8 and 32 characters long.')
            if not re.search(r'\d', v):
                raise ValueError('Password must contain at least one number.')
            if not re.search(r'[a-z]', v):
                raise ValueError('Password must contain at least one lowercase letter.')
            if not re.search(r'[A-Z]', v):
                raise ValueError('Password must contain at least one uppercase letter.')
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
                raise ValueError('Password must contain at least one special character.')
        return v

class DoctorEmployeeResponse(BasicInfoResponse):
    username: str
