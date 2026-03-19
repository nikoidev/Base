from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...core.config import settings
from ...core.database import get_db
from ...core.security import create_access_token
from ...schemas.token import Token
from ...schemas.user import UserResponse
from ...services.user_service import UserService
from ...utils.audit import AuditAction, AuditResource, log_action
from ..deps import get_current_active_user

router = APIRouter()


@router.post("/login", response_model=Token)
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
