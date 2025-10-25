import base64
import io
from typing import Optional

from PIL import Image
from pyzbar.pyzbar import decode as decode_barcode


def decode_from_base64(contents: str) -> Optional[dict]:
    """Decode barcode information from a dash upload base64 string."""
    try:
        content_header, content_string = contents.split(",")
    except ValueError as exc:
        raise ValueError("アップロードデータが不正です") from exc

    mime_type = content_header.replace("data:", "").split(";")[0]
    decoded = base64.b64decode(content_string)
    image = Image.open(io.BytesIO(decoded))
    barcodes = decode_barcode(image)

    if not barcodes:
        return None

    barcode = barcodes[0]
    return {
        "barcode": barcode.data.decode("utf-8"),
        "barcode_type": barcode.type,
        "image_bytes": decoded,
        "content_type": mime_type,
    }
