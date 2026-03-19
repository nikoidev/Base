from typing import Any, Dict, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.permission import Permission
from ..models.role import Role
from ..schemas.role import RoleCreate, RoleUpdate
from ..utils.pagination import paginate, validate_order_by

ALLOWED_ORDER_FIELDS = ["id", "name", "created_at"]


class RoleService:
    @staticmethod
    def get_role(db: Session, role_id: int) -> Optional[Role]:
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def get_role_by_name(db: Session, name: str) -> Optional[Role]:
        return db.query(Role).filter(Role.name == name).first()

    @staticmethod
    def get_roles(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: str = "id",
        order_desc: bool = False,
    ) -> Dict[str, Any]:
        """Get roles with pagination, search, filters, and sorting."""
        query = db.query(Role)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Role.name.ilike(search_filter),
                    Role.description.ilike(search_filter),
                )
            )

        if is_active is not None:
            query = query.filter(Role.is_active == is_active)

        safe_order_by = validate_order_by(order_by, ALLOWED_ORDER_FIELDS)
        order_column = getattr(Role, safe_order_by)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        return paginate(query, skip=skip, limit=limit)

    @staticmethod
    def create_role(db: Session, role: RoleCreate) -> Role:
        db_role = Role(
            name=role.name, description=role.description, is_active=role.is_active
        )

        if role.permission_ids:
            permissions = (
                db.query(Permission)
                .filter(Permission.id.in_(role.permission_ids))
                .all()
            )
            db_role.permissions = permissions

        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def update_role(db: Session, role_id: int, role: RoleUpdate) -> Optional[Role]:
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return None

        update_data = role.model_dump(exclude_unset=True)

        if "permission_ids" in update_data:
            permission_ids = update_data.pop("permission_ids")
            if permission_ids is not None:
                permissions = (
                    db.query(Permission).filter(Permission.id.in_(permission_ids)).all()
                )
                db_role.permissions = permissions

        for field, value in update_data.items():
            setattr(db_role, field, value)

        db.commit()
        db.refresh(db_role)
        return db_role

    @staticmethod
    def delete_role(db: Session, role_id: int) -> bool:
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return False
        db.delete(db_role)
        db.commit()
        return True
