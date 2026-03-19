from typing import Any, Dict, List, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.permission import Permission
from ..schemas.permission import PermissionCreate, PermissionUpdate


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
        """Get permissions with pagination, search, filters, and sorting"""
        query = db.query(Permission)

        # Search by name, code, or description
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Permission.name.ilike(search_filter),
                    Permission.code.ilike(search_filter),
                    Permission.description.ilike(search_filter),
                )
            )

        # Filter by resource
        if resource:
            query = query.filter(Permission.resource == resource)

        # Filter by action
        if action:
            query = query.filter(Permission.action == action)

        # Filter by active status
        if is_active is not None:
            query = query.filter(Permission.is_active == is_active)

        # Get total count
        total = query.count()

        # Sorting
        order_column = getattr(Permission, order_by, Permission.id)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        # Pagination
        items = query.offset(skip).limit(limit).all()

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
