from typing import Any, Dict, List, Optional

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from ..models.audit_log import AuditLog
from ..models.user import User
from ..utils.pagination import paginate, validate_order_by

ALLOWED_ORDER_FIELDS = ["id", "action", "resource", "created_at"]


class AuditLogService:
    @staticmethod
    def create_log(
        db: Session,
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> AuditLog:
        """Create an audit log entry."""
        log = AuditLog(
            user_id=user_id,
            action=action,
            resource=resource,
            resource_id=resource_id,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent,
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

    @staticmethod
    def get_logs(
        db: Session,
        skip: int = 0,
        limit: int = 50,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        search: Optional[str] = None,
        order_by: str = "created_at",
        order_desc: bool = True,
    ) -> Dict[str, Any]:
        """Get audit logs with pagination and filters."""
        query = db.query(AuditLog)

        if user_id:
            query = query.filter(AuditLog.user_id == user_id)

        if action:
            query = query.filter(AuditLog.action == action)

        if resource:
            query = query.filter(AuditLog.resource == resource)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    AuditLog.ip_address.ilike(search_filter),
                    AuditLog.user_agent.ilike(search_filter),
                )
            )

        safe_order_by = validate_order_by(order_by, ALLOWED_ORDER_FIELDS, default="created_at")
        order_column = getattr(AuditLog, safe_order_by)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        return paginate(query, skip=skip, limit=limit)

    @staticmethod
    def get_user_activity(db: Session, user_id: int, limit: int = 10) -> list[AuditLog]:
        """Get recent activity for a specific user."""
        return (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_recent_logs(db: Session, limit: int = 10) -> list[AuditLog]:
        """Get most recent audit logs (for dashboard)."""
        return db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()

    @staticmethod
    def enrich_log(log: AuditLog, user: Optional[User] = None) -> Dict[str, Any]:
        """Enrich an audit log with user information for API responses."""
        result = {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "resource": log.resource,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "user_agent": log.user_agent,
            "created_at": log.created_at,
        }
        if user:
            result["user_username"] = user.username
            result["user_email"] = user.email
        elif log.user:
            result["user_username"] = log.user.username
            result["user_email"] = log.user.email
        else:
            result["user_username"] = None
            result["user_email"] = None
        return result
