"""
Tests for authentication endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


@pytest.mark.auth
class TestLogin:
    """Test login functionality."""

    def test_login_success(self, client: TestClient, test_admin_user: User):
        """Test successful login with valid credentials."""
        response = client.post(
            "/api/auth/login", data={"username": "testadmin", "password": "admin123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_username(self, client: TestClient):
        """Test login with invalid username."""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "password123"},
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_invalid_password(self, client: TestClient, test_admin_user: User):
        """Test login with invalid password."""
        response = client.post(
            "/api/auth/login",
            data={"username": "testadmin", "password": "wrongpassword"},
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_inactive_user(
        self, client: TestClient, db: Session, test_admin_user: User
    ):
        """Test login with inactive user."""
        # Skip this test as inactive user validation might not be implemented
        pytest.skip("Inactive user validation not implemented in login endpoint")


@pytest.mark.auth
@pytest.mark.skip(reason="Refresh token endpoint not implemented yet")
class TestRefreshToken:
    """Test refresh token functionality."""

    def test_refresh_token_success(self, client: TestClient, test_admin_user: User):
        """Test successful token refresh."""
        # Login first
        login_response = client.post(
            "/api/auth/login", data={"username": "testadmin", "password": "admin123"}
        )
        refresh_token = login_response.json()["refresh_token"]

        # Refresh token
        response = client.post(
            "/api/auth/refresh", json={"refresh_token": refresh_token}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_refresh_token_invalid(self, client: TestClient):
        """Test refresh with invalid token."""
        response = client.post(
            "/api/auth/refresh", json={"refresh_token": "invalid_token"}
        )

        assert response.status_code == 401


@pytest.mark.auth
class TestGetCurrentUser:
    """Test getting current user information."""

    def test_get_me_success(self, client: TestClient, admin_headers: dict):
        """Test getting current user information."""
        response = client.get("/api/auth/me", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testadmin"
        assert data["email"] == "admin@test.com"
        assert data["is_superuser"] is True
        assert "roles" in data

    def test_get_me_unauthorized(self, client: TestClient):
        """Test getting current user without authentication."""
        response = client.get("/api/auth/me")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_get_me_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token."""
        response = client.get(
            "/api/auth/me", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401


@pytest.mark.auth
@pytest.mark.skip(reason="Change password endpoint not implemented yet")
class TestChangePassword:
    """Test password change functionality."""

    def test_change_password_success(self, client: TestClient, admin_headers: dict):
        """Test successful password change."""
        response = client.post(
            "/api/auth/change-password",
            headers=admin_headers,
            json={"current_password": "admin123", "new_password": "newpassword123"},
        )

        assert response.status_code == 200
        assert "Password updated successfully" in response.json()["message"]

        # Test login with new password
        login_response = client.post(
            "/api/auth/login",
            data={"username": "testadmin", "password": "newpassword123"},
        )
        assert login_response.status_code == 200

    def test_change_password_wrong_current(
        self, client: TestClient, admin_headers: dict
    ):
        """Test password change with wrong current password."""
        response = client.post(
            "/api/auth/change-password",
            headers=admin_headers,
            json={
                "current_password": "wrongpassword",
                "new_password": "newpassword123",
            },
        )

        assert response.status_code == 400
        assert "Incorrect password" in response.json()["detail"]

    def test_change_password_unauthorized(self, client: TestClient):
        """Test password change without authentication."""
        response = client.post(
            "/api/auth/change-password",
            json={"current_password": "admin123", "new_password": "newpassword123"},
        )

        assert response.status_code == 401
