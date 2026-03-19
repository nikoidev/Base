from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session

from ..models.audit_log import AuditLog
from ..models.user import User
from ..schemas.audit_log import AuditLogCreate


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
        """Create an audit log entry"""
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
        """Get audit logs with pagination and filters"""
        query = db.query(AuditLog)

        # Filters
        if user_id:
            query = query.filter(AuditLog.user_id == user_id)

        if action:
            query = query.filter(AuditLog.action == action)

        if resource:
            query = query.filter(AuditLog.resource == resource)

        # Search in details or IP
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    AuditLog.ip_address.ilike(search_filter),
                    AuditLog.user_agent.ilike(search_filter),
                )
            )

        # Get total count
        total = query.count()

        # Sorting (default: newest first)
        order_column = getattr(AuditLog, order_by, AuditLog.created_at)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        # Pagination
        items = query.offset(skip).limit(limit).all()

        # Calculate pagination info
        page = (skip // limit) + 1 if limit > 0 else 1
        pages = (total + limit - 1) // limit if limit > 0 else 1

        return {
            "items": items,
            "total": total,
            "page": page,
            "pages": pages,
            "limit": limit,
        }

    @staticmethod
    def get_user_activity(db: Session, user_id: int, limit: int = 10):
        """Get recent activity for a specific user"""
        return (
            db.query(AuditLog)
            .filter(AuditLog.user_id == user_id)
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_recent_logs(db: Session, limit: int = 10):
        """Get most recent audit logs (for dashboard)"""
        return db.query(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit).all()
