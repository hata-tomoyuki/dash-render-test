import uuid
from typing import Optional

from supabase import Client


def upload_to_storage(
    supabase: Client,
    file_bytes: bytes,
    original_filename: str,
    content_type: str,
) -> Optional[str]:
    file_ext = (original_filename or "jpg").split(".")[-1]
    file_name = f"{uuid.uuid4()}.{file_ext}"

    try:
        supabase.storage.from_("photos").upload(
            file_name,
            file_bytes,
            file_options={"content-type": content_type or f"image/{file_ext}"},
        )
    except Exception:
        try:
            supabase.storage.create_bucket("photos", options={"public": True})
            supabase.storage.from_("photos").upload(
                file_name,
                file_bytes,
                file_options={"content-type": content_type or f"image/{file_ext}"},
            )
        except Exception as exc:
            raise RuntimeError("画像のアップロードに失敗しました") from exc

    public_url = supabase.storage.from_("photos").get_public_url(file_name)
    return public_url


def insert_product_record(
    supabase: Client,
    barcode: str,
    barcode_type: str,
    product_name: str,
    image_url: str,
    description: str,
    tags: list = None,
    custom_tags: list = None,
    notes: str = None,
) -> None:
    data = {
        "barcode": barcode,
        "barcode_type": barcode_type,
        "product_name": product_name,
        "image_url": image_url,
        "description": description or "",
    }

    if tags:
        data["tags"] = tags
    if custom_tags:
        data["custom_tags"] = custom_tags
    if notes:
        data["notes"] = notes

    response = supabase.table("products").insert(data).execute()
    if getattr(response, "error", None):
        raise RuntimeError(response.error)


def delete_all_products(supabase: Client) -> None:
    response = (
        supabase.table("products")
        .delete()
        .neq("id", "00000000-0000-0000-0000-000000000000")
        .execute()
    )
    if getattr(response, "error", None):
        raise RuntimeError(response.error)


def get_all_products(supabase: Client):
    """Get all products from database"""
    response = (
        supabase.table("products").select("*").order("created_at", desc=True).execute()
    )
    if getattr(response, "error", None):
        raise RuntimeError(response.error)
    return response.data if hasattr(response, "data") else []


def get_product_stats(supabase: Client):
    """Get product statistics"""
    # Total products
    total_response = supabase.table("products").select("*").execute()
    total = (
        len(total_response.data)
        if hasattr(total_response, "data") and total_response.data
        else 0
    )

    # Unique barcodes
    unique_response = supabase.table("products").select("barcode").execute()
    unique_barcodes = (
        len(
            set(item["barcode"] for item in unique_response.data if item.get("barcode"))
        )
        if hasattr(unique_response, "data") and unique_response.data
        else 0
    )

    return {"total": total, "unique": unique_barcodes}
