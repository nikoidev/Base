from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...schemas.role import RoleCreate, RoleListResponse, RoleResponse, RoleUpdate
from ...services.role_service import RoleService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=RoleListResponse)
def read_roles(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name or description"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    order_by: str = Query("id", description="Field to order by"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    skip = (page - 1) * limit
    result = RoleService.get_roles(
        db,
        skip=skip,
        limit=limit,
        search=search,
        is_active=is_active,
        order_by=order_by,
        order_desc=order_desc,
    )
    return result


@router.get("/{role_id}", response_model=RoleResponse)
def read_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    role = RoleService.get_role(db, role_id=role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    # Check if role already exists
    db_role = RoleService.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=400, detail="Role name already registered")

    return RoleService.create_role(db=db, role=role)


@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    db_role = RoleService.update_role(db, role_id=role_id, role=role)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    success = RoleService.delete_role(db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return None
