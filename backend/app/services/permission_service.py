from typing import Any, Dict, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionUpdate
from ..utils.pagination import paginate, validate_order_by

ALLOWED_ORDER_FIELDS = ["id", "name", "code", "resource", "action", "created_at"]


class PermissionService:
    @staticmethod
    def get_permission(db: Session, permission_id: int) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.id == permission_id).first()

    @staticmethod
    def get_permission_by_code(db: Session, code: str) -> Optional[Permission]:
        return db.query(Permission).filter(Permission.code == code).first()

    @staticmethod
    def get_permissions(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        resource: Optional[str] = None,
        action: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: str = "id",
        order_desc: bool = False,
    ) -> Dict[str, Any]:
        """Get permissions with pagination, search, filters, and sorting."""
        query = db.query(Permission)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Permission.name.ilike(search_filter),
                    Permission.code.ilike(search_filter),
                    Permission.description.ilike(search_filter),
                )
            )

        if resource:
            query = query.filter(Permission.resource == resource)

        if action:
            query = query.filter(Permission.action == action)

        if is_active is not None:
            query = query.filter(Permission.is_active == is_active)

        safe_order_by = validate_order_by(order_by, ALLOWED_ORDER_FIELDS)
        order_column = getattr(Permission, safe_order_by)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        return paginate(query, skip=skip, limit=limit)

    @staticmethod
    def create_permission(db: Session, permission: PermissionCreate) -> Permission:
        db_permission = Permission(
            name=permission.name,
            code=permission.code,
            description=permission.description,
            resource=permission.resource,
            action=permission.action,
            is_active=permission.is_active,
        )
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)
        return db_permission

    @staticmethod
    def update_permission(
        db: Session, permission_id: int, permission: PermissionUpdate
    ) -> Optional[Permission]:
        db_permission = (
            db.query(Permission).filter(Permission.id == permission_id).first()
        )
        if not db_permission:
            return None

        update_data = permission.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permission, field, value)

        db.commit()
        db.refresh(db_permission)
        return db_permission

    @staticmethod
    def delete_permission(db: Session, permission_id: int) -> bool:
        db_permission = (
            db.query(Permission).filter(Permission.id == permission_id).first()
        )
        if not db_permission:
            return False
        db.delete(db_permission)
        db.commit()
        return True
