from __future__ import annotations
from http import HTTPStatus

from src.utils.image_factory import generate_image_bytes


def upload_attachment_bytes(
    api,
    *,
    filename: str,
    content_type: str,
    data: bytes,
    x_application_id: str | None = None,
    timeout_s: int = 60,
) -> int:
    headers = dict(api.session.headers)
    headers["Accept"] = "*/*"

    if x_application_id:
        headers["X-Application-ID"] = str(x_application_id)

    saved_ct = api.session.headers.pop("Content-Type", None)
    try:
        files = {"File": (filename, data, content_type)}
        r = api.session.post(api.base_url + "/attachments", files=files, headers=headers, timeout=timeout_s)
    finally:
        if saved_ct is not None:
            api.session.headers["Content-Type"] = saved_ct

    assert r.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), f"Upload failed: {r.status_code}, {r.text}"
    payload = r.json() if r.text else {}
    att_id = payload.get("id") if isinstance(payload, dict) else None
    assert att_id, f"No id in upload response: {payload}"
    return int(att_id)


def upload_generated_image(api, cfg, *, fmt: str = "png", label: str | None = None, width: int = 640, height: int = 360) -> int:
    gen = generate_image_bytes(fmt=fmt, width=width, height=height, label=label)
    return upload_attachment_bytes(
        api,
        filename=gen.filename,
        content_type=gen.content_type,
        data=gen.data,
        x_application_id=cfg.get("x_application_id"),
    )
