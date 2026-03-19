"""
RBAC (Role-Based Access Control) dependency for FastAPI routes.
Checks if the current user has the required permission code.
"""

from typing import Callable

from fastapi import Depends, HTTPException, status

from ..models.user import User
from .deps import get_current_active_user


def require_permission(permission_code: str) -> Callable:
    """
    FastAPI dependency that checks if the current user has a specific permission.

    Usage:
        @router.post("/", dependencies=[Depends(require_permission("user.create"))])
        def create_user(...):
            ...

    Superusers bypass all permission checks.
    """

    def permission_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        # Superusers bypass permission checks
        if current_user.is_superuser:
            return current_user

        # Collect all permission codes from the user's roles
        user_permissions: set[str] = set()
        for role in current_user.roles:
            for permission in role.permissions:
                user_permissions.add(permission.code)

        if permission_code not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{permission_code}' required",
            )

        return current_user

    return permission_checker
