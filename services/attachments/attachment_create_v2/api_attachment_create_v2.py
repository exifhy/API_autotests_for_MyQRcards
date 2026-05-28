from __future__ import annotations

from http import HTTPStatus
import time

import allure
import requests

from config.headers import Headers
from services.attachments.attachment_create_v2.endpoints import Endpoints
from services.attachments.attachment_create_v2.models.attachment_create_v2_model import AttachmentCreateV2Model
from src.constants.attributes import PHOTO_GALLERY_ATTRIBUTE_ID
from src.utils.image_factory import generate_image_bytes
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttachmentCreateV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Attachments/v2")
    def create_attachment_v2(
        self,
        *,
        label: str = "attachment_api_v2",
        fmt: str = "png",
        attribute_id: int = PHOTO_GALLERY_ATTRIBUTE_ID,
    ) -> AttachmentCreateV2Model:
        generated = generate_image_bytes(fmt=fmt, label=label)
        headers = Headers.auth_header(bearer_token=get_token())
        headers["Accept"] = "*/*"
        headers.pop("Content-Type", None)

        last_error: requests.RequestException | None = None
        for attempt in range(2):
            try:
                response = self._call(
                    "POST",
                    url=self.endpoints.create_attachment_v2_endpoint,
                    headers=headers,
                    data={
                        "AttributeID": str(attribute_id),
                        "Attachments.Index": "0",
                        "Attachments[0].IsIgnorePossibleDuplication": "true",
                    },
                    files={"Attachments[0].File": (generated.filename, generated.data, generated.content_type)},
                )
                break
            except requests.RequestException as exc:
                last_error = exc
                if attempt == 1:
                    raise
                time.sleep(1)
        else:
            raise last_error or RuntimeError("POST /Attachments/v2 failed without response")
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return AttachmentCreateV2Model(**response.json())
