"""
Script to reset the database - drops all tables and recreates them
"""
from sqlalchemy import text

from app.core.database import Base, SessionLocal, engine
from app.models import AuditLog, Permission, Role, User


def reset_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)

    # Also drop alembic_version table if using Alembic
    with engine.connect() as conn:
        try:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
            conn.commit()
            print("Alembic version table dropped")
        except Exception as e:
            print(f"Note: Could not drop alembic_version: {e}")

    print("Database reset successfully! Run init_db.py to reinitialize.")


if __name__ == "__main__":
    reset_db()
