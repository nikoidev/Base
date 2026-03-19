"""
Pytest configuration and fixtures for testing.
This file contains shared fixtures used across all tests.
"""
from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.main import app
from app.models.permission import Permission
from app.models.role import Role
from app.models.user import User

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database override.
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_permissions(db: Session) -> list[Permission]:
    """
    Create test permissions.
    """
    permissions_data = [
        {
            "name": "Crear Usuario",
            "code": "user.create",
            "resource": "users",
            "action": "create",
        },
        {
            "name": "Leer Usuario",
            "code": "user.read",
            "resource": "users",
            "action": "read",
        },
        {
            "name": "Actualizar Usuario",
            "code": "user.update",
            "resource": "users",
            "action": "update",
        },
        {
            "name": "Eliminar Usuario",
            "code": "user.delete",
            "resource": "users",
            "action": "delete",
        },
        {
            "name": "Crear Rol",
            "code": "role.create",
            "resource": "roles",
            "action": "create",
        },
        {
            "name": "Leer Rol",
            "code": "role.read",
            "resource": "roles",
            "action": "read",
        },
        {
            "name": "Actualizar Rol",
            "code": "role.update",
            "resource": "roles",
            "action": "update",
        },
        {
            "name": "Eliminar Rol",
            "code": "role.delete",
            "resource": "roles",
            "action": "delete",
        },
    ]

    permissions = []
    for perm_data in permissions_data:
        permission = Permission(**perm_data)
        db.add(permission)
        permissions.append(permission)

    db.commit()

    for p in permissions:
        db.refresh(p)

    return permissions


@pytest.fixture
def test_admin_role(db: Session, test_permissions: list[Permission]) -> Role:
    """
    Create an admin role with all permissions.
    """
    admin_role = Role(
        name="Administrador",
        description="Administrador con acceso completo",
        permissions=test_permissions,
    )
    db.add(admin_role)
    db.commit()
    db.refresh(admin_role)
    return admin_role


@pytest.fixture
def test_user_role(db: Session, test_permissions: list[Permission]) -> Role:
    """
    Create a user role with read permissions only.
    """
    read_permissions = [p for p in test_permissions if p.action == "read"]
    user_role = Role(
        name="Usuario",
        description="Usuario regular con acceso de lectura",
        permissions=read_permissions,
    )
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


@pytest.fixture
def test_admin_user(db: Session, test_admin_role: Role) -> User:
    """
    Create a test admin user.
    """
    user = User(
        email="admin@test.com",
        username="testadmin",
        hashed_password=get_password_hash("admin123"),
        first_name="Test",
        last_name="Admin",
        is_active=True,
        is_superuser=True,
        roles=[test_admin_role],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def test_regular_user(db: Session, test_user_role: Role) -> User:
    """
    Create a test regular user.
    """
    user = User(
        email="user@test.com",
        username="testuser",
        hashed_password=get_password_hash("user123"),
        first_name="Test",
        last_name="User",
        is_active=True,
        is_superuser=False,
        roles=[test_user_role],
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_token(client: TestClient, test_admin_user: User) -> str:
    """
    Get an authentication token for admin user.
    """
    response = client.post(
        "/api/auth/login", data={"username": "testadmin", "password": "admin123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def user_token(client: TestClient, test_regular_user: User) -> str:
    """
    Get an authentication token for regular user.
    """
    response = client.post(
        "/api/auth/login", data={"username": "testuser", "password": "user123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def admin_headers(admin_token: str) -> Dict[str, str]:
    """
    Get authorization headers for admin user.
    """
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture
def user_headers(user_token: str) -> Dict[str, str]:
    """
    Get authorization headers for regular user.
    """
    return {"Authorization": f"Bearer {user_token}"}
