from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, field_validator


class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = True
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = "America/Mexico_City"
    language: Optional[str] = "es"


class UserCreate(UserBase):
    password: str
    role_ids: Optional[List[int]] = []

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v: str) -> str:
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be 72 bytes or less")
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    role_ids: Optional[List[int]] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password_length_update(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if len(v.encode("utf-8")) > 72:
                raise ValueError("Password must be 72 bytes or less")
            if len(v) < 6:
                raise ValueError("Password must be at least 6 characters")
        return v


class ProfileUpdate(BaseModel):
    """Schema for users updating their own profile"""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    language: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class RoleInUser(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    roles: List[RoleInUser] = []

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """Paginated response for user list"""

    items: List[UserResponse]
    total: int
    page: int
    pages: int
    limit: int
