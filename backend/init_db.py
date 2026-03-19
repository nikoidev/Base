"""
Initialize database with Alembic migrations and seed data.
"""
import subprocess
import sys
from pathlib import Path

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models import Permission, Role, User


def run_migrations():
    """Apply all pending database migrations using Alembic."""
    print("Running database migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Migration failed: {result.stderr}")
        sys.exit(1)

    print("Migrations completed successfully")


def seed_data():
    """Seed initial data into the database."""
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Database already seeded")
            return

        print("Seeding initial data...")

        # Create default permissions
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
            {
                "name": "Crear Permiso",
                "code": "permission.create",
                "resource": "permissions",
                "action": "create",
            },
            {
                "name": "Leer Permiso",
                "code": "permission.read",
                "resource": "permissions",
                "action": "read",
            },
            {
                "name": "Actualizar Permiso",
                "code": "permission.update",
                "resource": "permissions",
                "action": "update",
            },
            {
                "name": "Eliminar Permiso",
                "code": "permission.delete",
                "resource": "permissions",
                "action": "delete",
            },
        ]

        permissions = []
        for perm_data in permissions_data:
            permission = Permission(**perm_data)
            db.add(permission)
            permissions.append(permission)

        db.commit()

        # Create admin role with all permissions
        admin_role = Role(
            name="Administrador",
            description="Administrador con acceso completo",
            permissions=permissions,
        )
        db.add(admin_role)

        # Create user role with read permissions
        user_permissions = [p for p in permissions if p.action == "read"]
        user_role = Role(
            name="Usuario",
            description="Usuario regular con acceso de lectura",
            permissions=user_permissions,
        )
        db.add(user_role)

        db.commit()

        # Create admin user
        admin_user = User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            is_active=True,
            is_superuser=True,
            roles=[admin_role],
        )
        db.add(admin_user)

        # Create regular user
        regular_user = User(
            email="user@example.com",
            username="user",
            hashed_password=get_password_hash("user123"),
            first_name="Regular",
            last_name="User",
            is_active=True,
            is_superuser=False,
            roles=[user_role],
        )
        db.add(regular_user)

        db.commit()

        print("✅ Database seeded successfully!")
        print("👤 Admin user: username='admin', password='admin123'")
        print("👤 Regular user: username='user', password='user123'")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """Initialize database with migrations and seed data."""
    print("🔧 Initializing database...")
    run_migrations()
    seed_data()
    print("✅ Database initialization complete!")


if __name__ == "__main__":
    init_db()
