from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_attribute_attachment_upload.endpoints import Endpoints
from services.cards.card_attribute_attachment_upload.models.card_attribute_attachment_upload_model import (
    CardAttributeAttachmentUploadModel,
)
from src.constants.attributes import FILE_ATTRIBUTE_ID, PHOTO_GALLERY_ATTRIBUTE_ID
from src.utils.image_factory import generate_image_bytes
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttributeAttachmentUploadAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /cards/{card_id}/upload/fromForm")
    def upload_card_attribute_attachment(
        self,
        card_id: int,
        card_attribute_id: int,
        *,
        attribute_id: int = PHOTO_GALLERY_ATTRIBUTE_ID,
        fmt: str = "png",
        label: str = "card_attr_upload",
    ) -> tuple[requests.Response, CardAttributeAttachmentUploadModel]:
        generated = generate_image_bytes(fmt=fmt, label=label)
        headers = Headers.auth_header(bearer_token=get_token())
        headers.pop("Content-Type", None)

        response = self._call(
            "PUT",
            url=self.endpoints.upload_card_attribute_attachment_endpoint.format(card_id=int(card_id)),
            headers=headers,
            data={
                "AttributeID": str(attribute_id),
                "CardAttributeID": str(card_attribute_id),
                "Attachments.Index": "0",
                "Attachments[0].IsIgnorePossibleDuplication": "true",
            },
            files={"Attachments[0].File": (generated.filename, generated.data, generated.content_type)},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.NO_CONTENT), (
            f"Expected 200/201/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, CardAttributeAttachmentUploadModel()

        return response, CardAttributeAttachmentUploadModel(**response.json())

    @allure.step("PUT /cards/{card_id}/upload/fromForm without auth")
    def upload_card_attribute_attachment_without_auth(self, card_id: int) -> requests.Response:
        generated = generate_image_bytes(fmt="png", label="no_auth")
        headers = Headers.without_authorization_field_header()
        headers.pop("Content-Type", None)

        response = self._call(
            "PUT",
            url=self.endpoints.upload_card_attribute_attachment_endpoint.format(card_id=int(card_id)),
            headers=headers,
            data={
                "AttributeID": str(PHOTO_GALLERY_ATTRIBUTE_ID),
                "Attachments.Index": "0",
                "Attachments[0].IsIgnorePossibleDuplication": "true",
            },
            files={"Attachments[0].File": (generated.filename, generated.data, generated.content_type)},
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
