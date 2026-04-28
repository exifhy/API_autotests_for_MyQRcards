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
