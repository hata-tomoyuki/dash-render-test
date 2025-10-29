"""Tag management service for color tags, category tags, and receipt location tags."""

from typing import Dict, List, Any, Optional
from services.supabase_client import get_supabase_client


def get_color_tags() -> List[Dict[str, Any]]:
    """Get all color tags."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        response = supabase.table("color_tag").select("*").execute()
        return response.data if response.data else []
    except Exception:
        return []


def get_category_tags() -> List[Dict[str, Any]]:
    """Get all category tags."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        response = supabase.table("category_tag").select("*").execute()
        return response.data if response.data else []
    except Exception:
        return []


def get_receipt_location_tags() -> List[Dict[str, Any]]:
    """Get all receipt location tags."""
    supabase = get_supabase_client()
    if not supabase:
        return []

    try:
        response = supabase.table("receipt_location").select("*").execute()
        return response.data if response.data else []
    except Exception:
        return []


def update_color_tag(color_tag_id: int, name: str, color: str) -> bool:
    """Update a color tag."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        supabase.table("color_tag").update(
            {"color_tag_name": name, "color_tag_color": color}
        ).eq("color_tag_id", color_tag_id).execute()
        return True
    except Exception:
        return False


def update_category_tag(category_tag_id: int, name: str, color: str, icon: str) -> bool:
    """Update a category tag."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        supabase.table("category_tag").update(
            {
                "category_tag_name": name,
                "category_tag_color": color,
                "category_tag_icon": icon,
            }
        ).eq("category_tag_id", category_tag_id).execute()
        return True
    except Exception:
        return False


def update_receipt_location_tag(receipt_location_id: int, name: str, icon: str) -> bool:
    """Update a receipt location tag."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        supabase.table("receipt_location").update(
            {"receipt_location_name": name, "receipt_location_icon": icon}
        ).eq("receipt_location_id", receipt_location_id).execute()
        return True
    except Exception:
        return False


def create_color_tag(name: str, color: str) -> bool:
    """Create a new color tag."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        supabase.table("color_tag").insert(
            {"color_tag_name": name, "color_tag_color": color}
        ).execute()
        return True
    except Exception:
        return False


def create_category_tag(name: str, color: str, icon: str) -> bool:
    """Create a new category tag."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        supabase.table("category_tag").insert(
            {
                "category_tag_name": name,
                "category_tag_color": color,
                "category_tag_icon": icon,
                "category_tag_use_flag": 1,
            }
        ).execute()
        return True
    except Exception:
        return False


def create_receipt_location_tag(name: str, icon: str) -> bool:
    """Create a new receipt location tag."""
    supabase = get_supabase_client()
    if not supabase:
        return False

    try:
        supabase.table("receipt_location").insert(
            {
                "receipt_location_name": name,
                "receipt_location_icon": icon,
                "receipt_location_use_flag": 1,
            }
        ).execute()
        return True
    except Exception:
        return False
