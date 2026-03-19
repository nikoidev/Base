from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class PermissionBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    is_active: Optional[bool] = True


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    resource: Optional[str] = None
    action: Optional[str] = None
    is_active: Optional[bool] = None


class PermissionResponse(PermissionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PermissionListResponse(BaseModel):
    """Paginated response for permission list"""

    items: List[PermissionResponse]
    total: int
    page: int
    pages: int
    limit: int
