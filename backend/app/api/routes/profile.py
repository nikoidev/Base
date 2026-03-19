import os
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.user import User
from ...schemas.user import ProfileUpdate, UserResponse
from ...services.user_service import UserService
from ...utils.audit import AuditAction, AuditResource, log_action
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user's profile"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    request: Request,
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update current user's profile (non-sensitive fields only)"""
    update_data = profile.model_dump(exclude_unset=True)

    # Store old values for audit
    old_values = {}
    for key in update_data.keys():
        old_values[key] = getattr(current_user, key, None)

    # Update user
    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)

    # Log the update
    log_action(
        db=db,
        request=request,
        user_id=current_user.id,  # type: ignore[arg-type]
        action=AuditAction.UPDATE,
        resource=AuditResource.PROFILE,
        resource_id=current_user.id,  # type: ignore[arg-type]
        details={
            "updated_fields": list(update_data.keys()),
            "old_values": old_values,
            "new_values": update_data,
        },
    )

    return current_user


@router.post("/upload-avatar")
async def upload_avatar(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Upload user avatar
    In production, this should upload to cloud storage (S3, Cloudinary, etc.)
    For now, we'll just return a placeholder URL
    """
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de archivo no permitido. Use JPEG, PNG, GIF o WebP.",
        )

    # Validate file size (max 5MB)
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > 5 * 1024 * 1024:  # 5MB
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo es demasiado grande. Máximo 5MB.",
            )

    # Reset file position
    await file.seek(0)

    # Create uploads directory if it doesn't exist
    uploads_dir = Path("uploads/avatars")
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = uploads_dir / unique_filename

    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # Generate URL (in production, this would be S3/Cloudinary URL)
    avatar_url = f"/uploads/avatars/{unique_filename}"

    # Update user avatar
    old_avatar = current_user.avatar_url
    current_user.avatar_url = avatar_url  # type: ignore[assignment]
    db.commit()

    # Log the change
    log_action(
        db=db,
        request=request,
        user_id=current_user.id,  # type: ignore[arg-type]
        action=AuditAction.UPDATE,
        resource=AuditResource.PROFILE,
        resource_id=current_user.id,  # type: ignore[arg-type]
        details={
            "field": "avatar_url",
            "old_value": old_avatar,
            "new_value": avatar_url,
        },
    )

    return {"message": "Avatar actualizado exitosamente", "avatar_url": avatar_url}


@router.delete("/avatar")
def delete_avatar(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete user avatar"""
    old_avatar = current_user.avatar_url

    # Delete file if exists
    if old_avatar and old_avatar.startswith("/uploads/"):
        file_path = Path(old_avatar.lstrip("/"))
        if file_path.exists():
            file_path.unlink()

    # Update database
    current_user.avatar_url = None
    db.commit()

    # Log the change
    log_action(
        db=db,
        request=request,
        user_id=current_user.id,  # type: ignore[arg-type]
        action=AuditAction.UPDATE,
        resource=AuditResource.PROFILE,
        resource_id=current_user.id,  # type: ignore[arg-type]
        details={"field": "avatar_url", "old_value": old_avatar, "action": "deleted"},
    )

    return {"message": "Avatar eliminado exitosamente"}
