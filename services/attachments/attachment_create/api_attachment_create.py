from __future__ import annotations

from http import HTTPStatus

import allure

from config.headers import Headers
from services.attachments.attachment_create.endpoints import Endpoints
from services.attachments.attachment_create.models.attachment_create_model import AttachmentCreateModel
from src.utils.image_factory import generate_image_bytes
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttachmentCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Attachments")
    def create_attachment(self, *, label: str = "attachment_api", fmt: str = "png") -> AttachmentCreateModel:
        generated = generate_image_bytes(fmt=fmt, label=label)
        headers = Headers.auth_header(bearer_token=get_token())
        headers["Accept"] = "*/*"
        headers.pop("Content-Type", None)

        response = self._call(
            "POST",
            url=self.endpoints.create_attachment_endpoint,
            headers=headers,
            files={"File": (generated.filename, generated.data, generated.content_type)},
        )
        assert response.status_code == HTTPStatus.CREATED, (
            f"Expected HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        return AttachmentCreateModel(**response.json())
