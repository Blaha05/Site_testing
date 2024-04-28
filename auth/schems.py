from typing import Optional
import uuid

from fastapi_users import schemas
from pydantic import EmailStr
from sqlalchemy import JSON


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    ful_mame: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    faculty: str
    course: str


