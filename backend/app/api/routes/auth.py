from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import select

from ...core.config import settings
from ...core.database import get_db
from ...core.security import (
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token,
    get_password_hash
)
from ...core.emails import send_reset_password_email
from ...models.user import User
from ...schemas.token import Token
from ...schemas.user import UserResponse
from ...schemas.auth import ForgotPassword, ResetPassword
from ...services.user_service import UserService
from ...utils.audit import AuditAction, AuditResource, log_action
from ...core.rate_limit import limiter
from ..deps import get_current_active_user

router = APIRouter()


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        # Log failed login attempt
        log_action(
            db=db,
            request=request,
            user_id=None,
            action=AuditAction.LOGIN_FAILED,
            resource=AuditResource.AUTH,
            details={"username": form_data.username},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Log successful login
    log_action(
        db=db,
        request=request,
        user_id=user.id,  # type: ignore[arg-type]
        action=AuditAction.LOGIN_SUCCESS,
        resource=AuditResource.AUTH,
        details={"username": user.username},
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user=Depends(get_current_active_user)):
    return current_user


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("3/minute")
def forgot_password(
    request: Request,
    payload: ForgotPassword,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate a password reset token and queue an email delivery.
    We always return 202 Accepted to prevent email enumeration.
    """
    user = db.scalar(select(User).where(User.email == payload.email))
    
    if user and user.is_active:
        token = create_password_reset_token(user.email)
        background_tasks.add_task(send_reset_password_email, user.email, token)
        
        # Log action
        log_action(
            db=db,
            request=request,
            user_id=user.id,
            action=AuditAction.PASSWORD_RESET_REQUESTED,
            resource=AuditResource.AUTH,
            details={"email": user.email}
        )
        
    return {"message": "Si el correo está registrado, recibirás un enlace de recuperación."}


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password(
    request: Request,
    payload: ResetPassword,
    db: Session = Depends(get_db)
):
    """
    Validate the token and update the user's password.
    """
    email = verify_password_reset_token(payload.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token inválido o expirado"
        )
        
    user = db.scalar(select(User).where(User.email == email))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o inactivo"
        )
        
    # Update password
    user.hashed_password = get_password_hash(payload.new_password)
    db.commit()
    
    log_action(
        db=db,
        request=request,
        user_id=user.id,
        action=AuditAction.PASSWORD_CHANGED,
        resource=AuditResource.AUTH,
        details={"via": "reset_token"}
    )
    
    return {"message": "Contraseña actualizada exitosamente"}
