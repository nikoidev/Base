from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import User
from ...schemas.audit_log import AuditLogListResponse, AuditLogResponse
from ...services.audit_log_service import AuditLogService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=AuditLogListResponse)
def get_audit_logs(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action"),
    resource: Optional[str] = Query(None, description="Filter by resource"),
    search: Optional[str] = Query(None, description="Search in IP or user agent"),
    order_by: str = Query("created_at", description="Field to order by"),
    order_desc: bool = Query(True, description="Order descending (newest first)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get audit logs with pagination and filters.
    Only accessible by authenticated users (typically admins).
    """
    skip = (page - 1) * limit
    result = AuditLogService.get_logs(
        db=db,
        skip=skip,
        limit=limit,
        user_id=user_id,
        action=action,
        resource=resource,
        search=search,
        order_by=order_by,
        order_desc=order_desc,
    )

    # Enrich with user information
    enriched_items = []
    for log in result["items"]:
        log_dict = {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at,
            "user_username": log.user.username if log.user else None,
            "user_email": log.user.email if log.user else None,
        }
        enriched_items.append(log_dict)

    return {
        "items": enriched_items,
        "total": result["total"],
        "page": result["page"],
        "pages": result["pages"],
        "limit": result["limit"],
    }


@router.get("/recent", response_model=list[AuditLogResponse])
def get_recent_logs(
    limit: int = Query(10, ge=1, le=50, description="Number of recent logs"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get most recent audit logs (for dashboard widget)"""
    logs = AuditLogService.get_recent_logs(db=db, limit=limit)

    enriched_logs = []
    for log in logs:
        log_dict = {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at,
            "user_username": log.user.username if log.user else None,
            "user_email": log.user.email if log.user else None,
        }
        enriched_logs.append(log_dict)

    return enriched_logs


@router.get("/my-activity", response_model=list[AuditLogResponse])
def get_my_activity(
    limit: int = Query(20, ge=1, le=100, description="Number of activities"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get current user's recent activity"""
    logs = AuditLogService.get_user_activity(
        db=db, user_id=current_user.id, limit=limit  # type: ignore[arg-type]
    )

    enriched_logs = []
    for log in logs:
        log_dict = {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at,
            "user_username": current_user.username,
            "user_email": current_user.email,
        }
        enriched_logs.append(log_dict)

    return enriched_logs
