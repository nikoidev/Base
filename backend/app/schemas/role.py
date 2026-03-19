from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[int]] = None


class PermissionInRole(BaseModel):
    id: int
    name: str
    code: str
    resource: Optional[str] = None
    action: Optional[str] = None

    class Config:
        from_attributes = True


class RoleResponse(RoleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    permissions: List[PermissionInRole] = []

    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """Paginated response for role list"""

    items: List[RoleResponse]
    total: int
    page: int
    pages: int
    limit: int
