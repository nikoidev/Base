from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    action = Column(
        String(50), nullable=False, index=True
    )  # CREATE, UPDATE, DELETE, LOGIN, etc.
    resource = Column(
        String(50), nullable=False, index=True
    )  # users, roles, permissions, etc.
    resource_id = Column(Integer, nullable=True)  # ID del recurso afectado
    details = Column(JSON, nullable=True)  # Detalles adicionales en formato JSON
    ip_address = Column(String(45), nullable=True)  # IPv4 o IPv6
    user_agent = Column(String(255), nullable=True)  # Browser/Device info
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relationship
    user = relationship("User", foreign_keys=[user_id])

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource})>"
        )
