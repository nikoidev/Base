from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.permission import (
    PermissionCreate,
    PermissionListResponse,
    PermissionResponse,
    PermissionUpdate,
)
from ...services.permission_service import PermissionService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=PermissionListResponse)
def read_permissions(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(
        None, description="Search by name, code, or description"
    ),
    resource: Optional[str] = Query(None, description="Filter by resource"),
    action: Optional[str] = Query(None, description="Filter by action"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    order_by: str = Query("id", description="Field to order by"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    skip = (page - 1) * limit
    result = PermissionService.get_permissions(
        db,
        skip=skip,
        limit=limit,
        search=search,
        resource=resource,
        action=action,
        is_active=is_active,
        order_by=order_by,
        order_desc=order_desc,
    )
    return result


@router.get("/{permission_id}", response_model=PermissionResponse)
def read_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    permission = PermissionService.get_permission(db, permission_id=permission_id)
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission


@router.post(
    "/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED
)
def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    # Check if permission code already exists
    db_permission = PermissionService.get_permission_by_code(db, code=permission.code)
    if db_permission:
        raise HTTPException(
            status_code=400, detail="Permission code already registered"
        )

    return PermissionService.create_permission(db=db, permission=permission)


@router.put("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: int,
    permission: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    db_permission = PermissionService.update_permission(
        db, permission_id=permission_id, permission=permission
    )
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    success = PermissionService.delete_permission(db, permission_id=permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return None
