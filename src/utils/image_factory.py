from __future__ import annotations

import io
import time
import uuid
from dataclasses import dataclass
from typing import Literal

from PIL import Image, ImageDraw, ImageFont


@dataclass(frozen=True)
class GeneratedFile:
    filename: str
    content_type: str
    data: bytes


def generate_image_bytes(
    *,
    fmt: Literal["png", "jpeg"] = "png",
    width: int = 640,
    height: int = 360,
    label: str | None = None,
) -> GeneratedFile:
    img = Image.new("RGB", (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)

    stamp = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    text = label or f"autotest {stamp}"

    try:
        font = ImageFont.load_default()
    except Exception:
        font = None

    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(60, 60, 60), width=3)
    draw.text((40, 40), text, fill=(20, 20, 20), font=font)

    bio = io.BytesIO()
    if fmt == "png":
        img.save(bio, format="PNG")
        return GeneratedFile(
            filename=f"autotest_{stamp}.png",
            content_type="image/png",
            data=bio.getvalue(),
        )

    img.save(bio, format="JPEG", quality=90)
    return GeneratedFile(
        filename=f"autotest_{stamp}.jpg",
        content_type="image/jpeg",
        data=bio.getvalue(),
    )


def generate_large_image_bytes(*, target_size_mb: float = 2.0) -> GeneratedFile:
    """Generate an uncompressed PNG image guaranteed to exceed target_size_mb."""
    import math
    pixels_needed = int(target_size_mb * 1024 * 1024 / 3)
    side = math.ceil(math.sqrt(pixels_needed))

    stamp = f"{int(time.time())}_{uuid.uuid4().hex[:8]}"
    img = Image.new("RGB", (side, side), color=(200, 100, 50))
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), f"large-autotest {stamp}", fill=(0, 0, 0))

    bio = io.BytesIO()
    img.save(bio, format="PNG", compress_level=0)
    return GeneratedFile(
        filename=f"large_autotest_{stamp}.png",
        content_type="image/png",
        data=bio.getvalue(),
    )
