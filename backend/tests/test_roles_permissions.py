"""
Tests for roles and permissions CRUD operations.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role


@pytest.mark.roles
@pytest.mark.integration
class TestGetRoles:
    """Test getting roles list."""

    def test_get_roles_success(
        self, client: TestClient, admin_headers: dict, test_admin_role: Role
    ):
        """Test getting all roles."""
        response = client.get("/api/roles/", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 1

    def test_get_roles_with_pagination(self, client: TestClient, admin_headers: dict):
        """Test getting roles with pagination."""
        response = client.get("/api/roles/?skip=0&limit=10", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data


@pytest.mark.roles
@pytest.mark.integration
class TestGetRole:
    """Test getting single role."""

    def test_get_role_by_id(
        self, client: TestClient, admin_headers: dict, test_admin_role: Role
    ):
        """Test getting role by ID."""
        response = client.get(f"/api/roles/{test_admin_role.id}", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_admin_role.id
        assert data["name"] == test_admin_role.name
        assert "permissions" in data

    def test_get_nonexistent_role(self, client: TestClient, admin_headers: dict):
        """Test getting nonexistent role."""
        response = client.get("/api/roles/99999", headers=admin_headers)

        assert response.status_code == 404


@pytest.mark.roles
@pytest.mark.integration
class TestCreateRole:
    """Test creating roles."""

    def test_create_role_success(
        self,
        client: TestClient,
        admin_headers: dict,
        test_permissions: list[Permission],
    ):
        """Test creating a new role."""
        role_data = {
            "name": "Editor",
            "description": "Editor role",
            "permission_ids": [test_permissions[0].id, test_permissions[1].id],
        }

        response = client.post("/api/roles/", headers=admin_headers, json=role_data)

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == role_data["name"]
        assert data["description"] == role_data["description"]
        assert len(data["permissions"]) == 2

    def test_create_role_duplicate_name(
        self, client: TestClient, admin_headers: dict, test_admin_role: Role
    ):
        """Test creating role with duplicate name."""
        role_data = {
            "name": test_admin_role.name,  # Duplicate
            "description": "Duplicate role",
            "permission_ids": [],
        }

        response = client.post("/api/roles/", headers=admin_headers, json=role_data)

        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "already" in detail or "registered" in detail


@pytest.mark.roles
@pytest.mark.integration
class TestUpdateRole:
    """Test updating roles."""

    def test_update_role_success(
        self, client: TestClient, admin_headers: dict, test_user_role: Role
    ):
        """Test updating role information."""
        update_data = {"name": "Updated Role", "description": "Updated description"}

        response = client.put(
            f"/api/roles/{test_user_role.id}", headers=admin_headers, json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["description"] == update_data["description"]

    def test_update_role_permissions(
        self,
        client: TestClient,
        admin_headers: dict,
        test_user_role: Role,
        test_permissions: list[Permission],
    ):
        """Test updating role permissions."""
        update_data = {"permission_ids": [test_permissions[0].id]}

        response = client.put(
            f"/api/roles/{test_user_role.id}", headers=admin_headers, json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["permissions"]) == 1


@pytest.mark.roles
@pytest.mark.integration
class TestDeleteRole:
    """Test deleting roles."""

    def test_delete_role_success(
        self, client: TestClient, admin_headers: dict, db: Session
    ):
        """Test deleting a role."""
        # Create a role to delete
        role = Role(name="ToDelete", description="Role to delete")
        db.add(role)
        db.commit()
        db.refresh(role)

        response = client.delete(f"/api/roles/{role.id}", headers=admin_headers)

        assert response.status_code in [200, 204]
        if response.status_code == 200:
            assert "deleted successfully" in response.json()["message"]


@pytest.mark.permissions
@pytest.mark.integration
class TestGetPermissions:
    """Test getting permissions list."""

    def test_get_permissions_success(
        self,
        client: TestClient,
        admin_headers: dict,
        test_permissions: list[Permission],
    ):
        """Test getting all permissions."""
        response = client.get("/api/permissions/", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= len(test_permissions)

    def test_get_permissions_filter_by_resource(
        self, client: TestClient, admin_headers: dict
    ):
        """Test filtering permissions by resource."""
        response = client.get("/api/permissions/?resource=users", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert all(p["resource"] == "users" for p in data["items"])

    def test_get_permissions_filter_by_action(
        self, client: TestClient, admin_headers: dict
    ):
        """Test filtering permissions by action."""
        response = client.get("/api/permissions/?action=read", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert all(p["action"] == "read" for p in data["items"])


@pytest.mark.permissions
@pytest.mark.integration
class TestGetPermission:
    """Test getting single permission."""

    def test_get_permission_by_id(
        self,
        client: TestClient,
        admin_headers: dict,
        test_permissions: list[Permission],
    ):
        """Test getting permission by ID."""
        perm = test_permissions[0]
        response = client.get(f"/api/permissions/{perm.id}", headers=admin_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == perm.id
        assert data["code"] == perm.code


@pytest.mark.permissions
@pytest.mark.integration
class TestCreatePermission:
    """Test creating permissions."""

    def test_create_permission_success(self, client: TestClient, admin_headers: dict):
        """Test creating a new permission."""
        perm_data = {
            "name": "Test Permission",
            "code": "test.permission",
            "resource": "test",
            "action": "test",
        }

        response = client.post(
            "/api/permissions/", headers=admin_headers, json=perm_data
        )

        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == perm_data["name"]
        assert data["code"] == perm_data["code"]

    def test_create_permission_duplicate_code(
        self,
        client: TestClient,
        admin_headers: dict,
        test_permissions: list[Permission],
    ):
        """Test creating permission with duplicate code."""
        perm_data = {
            "name": "Duplicate",
            "code": test_permissions[0].code,  # Duplicate
            "resource": "test",
            "action": "test",
        }

        response = client.post(
            "/api/permissions/", headers=admin_headers, json=perm_data
        )

        assert response.status_code == 400
        detail = response.json()["detail"].lower()
        assert "already" in detail or "registered" in detail


@pytest.mark.permissions
@pytest.mark.integration
class TestUpdatePermission:
    """Test updating permissions."""

    def test_update_permission_success(
        self,
        client: TestClient,
        admin_headers: dict,
        test_permissions: list[Permission],
    ):
        """Test updating permission information."""
        perm = test_permissions[0]
        update_data = {
            "name": "Updated Permission Name",
            "description": "Updated description",
        }

        response = client.put(
            f"/api/permissions/{perm.id}", headers=admin_headers, json=update_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]


@pytest.mark.permissions
@pytest.mark.integration
class TestDeletePermission:
    """Test deleting permissions."""

    def test_delete_permission_success(
        self, client: TestClient, admin_headers: dict, db: Session
    ):
        """Test deleting a permission."""
        # Create a permission to delete
        perm = Permission(
            name="To Delete", code="to.delete", resource="test", action="delete"
        )
        db.add(perm)
        db.commit()
        db.refresh(perm)

        response = client.delete(f"/api/permissions/{perm.id}", headers=admin_headers)

        assert response.status_code in [200, 204]
