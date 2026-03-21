from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.routes import audit_logs, auth, permissions, profile, roles, users
from .core.config import settings
from .core.database import Base, engine
from .core.rate_limit import limiter
from .core.logger import setup_logging
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize structured logger upon startup
    setup_logging()
    yield

app = FastAPI(
    title="User Management System API",
    description="Complete CRUD API for Users, Roles, and Permissions with Audit Log",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory if it doesn't exist
uploads_dir = Path("uploads")
uploads_dir.mkdir(exist_ok=True)

# Serve uploaded files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(roles.router, prefix="/api/roles", tags=["Roles"])
app.include_router(permissions.router, prefix="/api/permissions", tags=["Permissions"])
app.include_router(audit_logs.router, prefix="/api/audit-logs", tags=["Audit Logs"])
app.include_router(profile.router, prefix="/api/profile", tags=["Profile"])


@app.get("/")
def root():
    return {
        "message": "User Management System API",
        "version": "2.0.0",
        "docs": "/docs",
    }
