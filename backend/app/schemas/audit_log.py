from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AuditLogBase(BaseModel):
    action: str
    resource: str
    resource_id: Optional[int] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    user_id: Optional[int] = None


class AuditLogResponse(AuditLogBase):
    id: int
    user_id: Optional[int] = None
    created_at: datetime

    # User info (optional, for frontend display)
    user_username: Optional[str] = None
    user_email: Optional[str] = None

    class Config:
        from_attributes = True


class AuditLogListResponse(BaseModel):
    """Paginated response for audit log list"""

    items: List[AuditLogResponse]
    total: int
    page: int
    pages: int
    limit: int
