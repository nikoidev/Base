"""
Shared pagination utilities to avoid code duplication across services.
"""

from typing import Any, Dict

from sqlalchemy.orm import Query


def paginate(
    query: Query,
    skip: int = 0,
    limit: int = 100,
) -> Dict[str, Any]:
    """
    Apply pagination to a SQLAlchemy query and return results with metadata.

    Returns:
        Dict with keys: items, total, page, pages, limit
    """
    total = query.count()
    items = query.offset(skip).limit(limit).all()

    page = (skip // limit) + 1 if limit > 0 else 1
    pages = (total + limit - 1) // limit if limit > 0 else 1

    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": pages,
        "limit": limit,
    }


def validate_order_by(order_by: str, allowed_fields: list[str], default: str = "id") -> str:
    """
    Validate that order_by is in the allowed fields list.
    Returns the validated field or the default.
    """
    if order_by in allowed_fields:
        return order_by
    return default
