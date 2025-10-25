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


def insert_photo_record(
    supabase: Client,
    barcode: str,
    barcode_type: str,
    image_url: str,
    description: str,
) -> None:
    response = (
        supabase.table("photos")
        .insert(
            {
                "barcode": barcode,
                "barcode_type": barcode_type,
                "image_url": image_url,
                "description": description or "",
            }
        )
        .execute()
    )
    if getattr(response, "error", None):
        raise RuntimeError(response.error)


def delete_all_photos(supabase: Client) -> None:
    response = (
        supabase.table("photos")
        .delete()
        .neq("id", "00000000-0000-0000-0000-000000000000")
        .execute()
    )
    if getattr(response, "error", None):
        raise RuntimeError(response.error)
