"""Utility for decoding base64 images from Jupyter notebook cells."""

import base64
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def decode_and_save_image(
    data: dict[str, Any], img_dir: Path, base_name: str, image_counter: int
) -> tuple[bool, str | None, Path | None]:
    """Decode a base64 image from cell data and save it.

    Returns:
        Tuple of (success, img_ext, img_path)
    """
    if "image/png" not in data and "application/pdf" not in data:
        return False, None, None

    img_ext = "pdf" if "application/pdf" in data else "png"
    img_data = data.get("application/pdf") or data.get("image/png")

    if img_data is None:
        return False, None, None

    if isinstance(img_data, list):
        img_data = "".join(img_data)

    if not isinstance(img_data, str):
        return False, None, None

    img_filename = f"{base_name}_fig_{image_counter}.{img_ext}"
    img_path = img_dir / img_filename

    try:
        img_bytes = base64.b64decode(img_data)
        with open(img_path, "wb") as img_file:
            img_file.write(img_bytes)
        return True, img_ext, img_path
    except Exception as e:
        logger.error(f"Failed to decode image: {e}")
        return False, None, None
