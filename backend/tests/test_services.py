"""
Unit tests for service layer functions.
"""
import pytest
from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.user import User
from app.schemas.permission import PermissionCreate
from app.schemas.role import RoleCreate, RoleUpdate
from app.schemas.user import UserCreate, UserUpdate
from app.services.permission_service import PermissionService
from app.services.role_service import RoleService
from app.services.user_service import UserService


@pytest.mark.unit
class TestUserService:
    """Test UserService methods."""

    def test_get_user(self, db: Session, test_admin_user: User):
        """Test getting user by ID."""
        user = UserService.get_user(db, test_admin_user.id)

        assert user is not None
        assert user.id == test_admin_user.id
        assert user.username == test_admin_user.username

    def test_get_user_by_email(self, db: Session, test_admin_user: User):
        """Test getting user by email."""
        user = UserService.get_user_by_email(db, test_admin_user.email)

        assert user is not None
        assert user.email == test_admin_user.email

    def test_get_user_by_username(self, db: Session, test_admin_user: User):
        """Test getting user by username."""
        user = UserService.get_user_by_username(db, test_admin_user.username)

        assert user is not None
        assert user.username == test_admin_user.username

    def test_get_users_with_search(
        self, db: Session, test_admin_user: User, test_regular_user: User
    ):
        """Test getting users with search."""
        result = UserService.get_users(db, search="testadmin")

        assert result["total"] >= 1
        assert any(u.username == "testadmin" for u in result["items"])

    def test_get_users_with_role_filter(
        self, db: Session, test_admin_user: User, test_admin_role: Role
    ):
        """Test filtering users by role."""
        result = UserService.get_users(db, role_id=test_admin_role.id)

        assert result["total"] >= 1
        assert all(
            any(r.id == test_admin_role.id for r in u.roles) for u in result["items"]
        )

    def test_create_user(self, db: Session, test_user_role: Role):
        """Test creating a new user."""
        user_data = UserCreate(
            email="newuser@test.com",
            username="newuser",
            password="password123",
            first_name="New",
            last_name="User",
            role_ids=[test_user_role.id],
        )

        user = UserService.create_user(db, user_data)

        assert user.id is not None
        assert user.email == user_data.email
        assert user.username == user_data.username
        assert len(user.roles) == 1

    def test_update_user(self, db: Session, test_regular_user: User):
        """Test updating user."""
        update_data = UserUpdate(first_name="Updated", last_name="Name")

        updated_user = UserService.update_user(db, test_regular_user.id, update_data)

        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"

    def test_delete_user(self, db: Session, test_user_role: Role):
        """Test deleting user."""
        # Create user to delete
        user = User(
            email="delete@test.com",
            username="deleteuser",
            hashed_password="hashed",
            roles=[test_user_role],
        )
        db.add(user)
        db.commit()
        user_id = user.id

        # Delete user
        result = UserService.delete_user(db, user_id)

        assert result is True

        # Verify deletion
        deleted_user = UserService.get_user(db, user_id)
        assert deleted_user is None


@pytest.mark.unit
class TestRoleService:
    """Test RoleService methods."""

    def test_get_role(self, db: Session, test_admin_role: Role):
        """Test getting role by ID."""
        role = RoleService.get_role(db, test_admin_role.id)

        assert role is not None
        assert role.id == test_admin_role.id
        assert role.name == test_admin_role.name

    def test_get_role_by_name(self, db: Session, test_admin_role: Role):
        """Test getting role by name."""
        role = RoleService.get_role_by_name(db, test_admin_role.name)

        assert role is not None
        assert role.name == test_admin_role.name

    def test_get_roles(self, db: Session, test_admin_role: Role, test_user_role: Role):
        """Test getting all roles."""
        result = RoleService.get_roles(db)

        assert result["total"] >= 2
        assert len(result["items"]) >= 2

    def test_create_role(self, db: Session, test_permissions):
        """Test creating a new role."""
        role_data = RoleCreate(
            name="Test Role",
            description="Test role description",
            permission_ids=[test_permissions[0].id],
        )

        role = RoleService.create_role(db, role_data)

        assert role.id is not None
        assert role.name == role_data.name
        assert len(role.permissions) == 1

    def test_update_role(self, db: Session, test_user_role: Role):
        """Test updating role."""
        update_data = RoleUpdate(name="Updated Role", description="Updated description")

        updated_role = RoleService.update_role(db, test_user_role.id, update_data)

        assert updated_role.name == "Updated Role"
        assert updated_role.description == "Updated description"

    def test_delete_role(self, db: Session):
        """Test deleting role."""
        # Create role to delete
        role = Role(name="ToDelete", description="Delete me")
        db.add(role)
        db.commit()
        role_id = role.id

        # Delete role
        result = RoleService.delete_role(db, role_id)

        assert result is True

        # Verify deletion
        deleted_role = RoleService.get_role(db, role_id)
        assert deleted_role is None


@pytest.mark.unit
class TestPermissionService:
    """Test PermissionService methods."""

    def test_get_permission(self, db: Session, test_permissions):
        """Test getting permission by ID."""
        perm = test_permissions[0]
        result = PermissionService.get_permission(db, perm.id)

        assert result is not None
        assert result.id == perm.id
        assert result.code == perm.code

    def test_get_permission_by_code(self, db: Session, test_permissions):
        """Test getting permission by code."""
        perm = test_permissions[0]
        result = PermissionService.get_permission_by_code(db, perm.code)

        assert result is not None
        assert result.code == perm.code

    def test_get_permissions_with_filter(self, db: Session, test_permissions):
        """Test getting permissions with resource filter."""
        result = PermissionService.get_permissions(db, resource="users")

        assert result["total"] >= 1
        assert all(p.resource == "users" for p in result["items"])

    def test_create_permission(self, db: Session):
        """Test creating a new permission."""
        perm_data = PermissionCreate(
            name="Test Permission",
            code="test.permission",
            resource="test",
            action="test",
        )

        perm = PermissionService.create_permission(db, perm_data)

        assert perm.id is not None
        assert perm.name == perm_data.name
        assert perm.code == perm_data.code

    def test_delete_permission(self, db: Session, test_permissions):
        """Test deleting permission."""
        # Use one of the test permissions
        perm_id = test_permissions[-1].id

        result = PermissionService.delete_permission(db, perm_id)

        assert result is True

        # Verify deletion
        deleted_perm = PermissionService.get_permission(db, perm_id)
        assert deleted_perm is None
