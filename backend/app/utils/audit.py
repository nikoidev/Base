from typing import Any, Dict, Optional

from fastapi import Request
from sqlalchemy.orm import Session

from ..services.audit_log_service import AuditLogService


def log_action(
    db: Session,
    request: Request,
    user_id: Optional[int],
    action: str,
    resource: str,
    resource_id: Optional[int] = None,
    details: Optional[Dict[str, Any]] = None,
):
    """Helper function to log actions"""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    AuditLogService.create_log(
        db=db,
        user_id=user_id,
        action=action,
        resource=resource,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
    )


# Action constants
class AuditAction:
    # Auth actions
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILED = "LOGIN_FAILED"
    LOGOUT = "LOGOUT"
    PASSWORD_CHANGED = "PASSWORD_CHANGED"
    PASSWORD_RESET_REQUESTED = "PASSWORD_RESET_REQUESTED"
    PASSWORD_RESET = "PASSWORD_RESET"

    # CRUD actions
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    # Specific actions
    ROLE_ASSIGNED = "ROLE_ASSIGNED"
    ROLE_REMOVED = "ROLE_REMOVED"
    PERMISSION_GRANTED = "PERMISSION_GRANTED"
    PERMISSION_REVOKED = "PERMISSION_REVOKED"
    USER_ACTIVATED = "USER_ACTIVATED"
    USER_DEACTIVATED = "USER_DEACTIVATED"


# Resource constants
class AuditResource:
    USER = "user"
    ROLE = "role"
    PERMISSION = "permission"
    AUTH = "auth"
    PROFILE = "profile"
