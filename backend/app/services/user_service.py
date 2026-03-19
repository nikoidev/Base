from typing import Any, Dict, Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..core.security import get_password_hash, verify_password
from ..models.role import Role
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..utils.pagination import paginate, validate_order_by

ALLOWED_ORDER_FIELDS = ["id", "username", "email", "first_name", "last_name", "created_at"]


class UserService:
    @staticmethod
    def get_user(db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        order_by: str = "id",
        order_desc: bool = False,
    ) -> Dict[str, Any]:
        """Get users with pagination, search, filters, and sorting."""
        query = db.query(User)

        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    User.username.ilike(search_filter),
                    User.email.ilike(search_filter),
                    User.first_name.ilike(search_filter),
                    User.last_name.ilike(search_filter),
                )
            )

        if role_id:
            query = query.join(User.roles).filter(Role.id == role_id)

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        # Sorting with validated order_by
        safe_order_by = validate_order_by(order_by, ALLOWED_ORDER_FIELDS)
        order_column = getattr(User, safe_order_by)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())

        return paginate(query, skip=skip, limit=limit)

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
        )

        if user.role_ids:
            roles = db.query(Role).filter(Role.id.in_(user.role_ids)).all()
            db_user.roles = roles

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return None

        update_data = user.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        if "role_ids" in update_data:
            role_ids = update_data.pop("role_ids")
            if role_ids is not None:
                roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
                db_user.roles = roles

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            return False
        db.delete(db_user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):  # type: ignore
            return None
        return user
