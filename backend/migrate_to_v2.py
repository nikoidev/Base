"""
Migration script to add new fields to users table and create audit_logs table
Run this after updating the models
"""
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine, SessionLocal, Base
from app.models import AuditLog

def migrate():
    """Run database migrations"""
    print("Starting migration to v2.0...")
    
    db = SessionLocal()
    
    try:
        # Add new columns to users table
        print("Adding new columns to users table...")
        migrations = [
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS bio VARCHAR(500)",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS timezone VARCHAR(50) DEFAULT 'America/Mexico_City'",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS language VARCHAR(10) DEFAULT 'es'",
        ]
        
        for migration in migrations:
            try:
                db.execute(text(migration))
                db.commit()
                print(f"[OK] Executed: {migration[:50]}...")
            except Exception as e:
                print(f"[SKIP] Error or already exists: {migration[:50]}...")
                db.rollback()
        
        # Create audit_logs table using SQLAlchemy
        print("\nCreating audit_logs table...")
        Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables.get('audit_logs')])
        print("[OK] audit_logs table created")
        
        print("\n[SUCCESS] Migration completed successfully!")
        print("\nNew features available:")
        print("  - User profile fields (phone, avatar, bio, timezone, language)")
        print("  - Audit log system")
        
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    migrate()

