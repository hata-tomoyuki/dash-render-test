from typing import Any, Dict, List

# In-memory storage for demo purposes when Supabase is not available
PHOTOS_STORAGE: List[Dict[str, Any]] = []


def get_supabase_client():
    """Get Supabase client - lazy import to avoid circular imports"""
    from services.supabase_client import get_supabase_client as _get_client
    return _get_client()


def _fetch_home_metrics() -> Dict[str, int]:
    try:
        from services.photo_service import get_product_stats
        supabase = get_supabase_client()
        return get_product_stats(supabase)
    except Exception:
        return {"total": 0, "unique": 0}


def _fetch_photos() -> List[Dict[str, Any]]:
    try:
        from services.photo_service import get_all_products
        supabase = get_supabase_client()
        return get_all_products(supabase)
    except Exception:
        return PHOTOS_STORAGE.copy()  # Fallback to in-memory storage


def _fetch_total_photos() -> int:
    return len(_fetch_photos())
