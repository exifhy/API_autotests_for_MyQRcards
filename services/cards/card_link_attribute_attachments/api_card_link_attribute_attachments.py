from http import HTTPStatus

import allure
import requests

from services.cards.card_attribute_attachments.models.card_attribute_attachments_model import (
    CardAttributeAttachmentItemModel,
    CardAttributeAttachmentsModel,
)
from services.cards.card_link_attribute_attachments.endpoints import Endpoints
from src.support.helper import Helper


class CardLinkAttributeAttachmentsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /cards/{token}/cardLink/attributes/attachments")
    def get_card_link_attribute_attachments(
        self,
        token: str,
    ) -> tuple[requests.Response, CardAttributeAttachmentsModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_card_link_attribute_attachments_endpoint.format(token=token),
            headers={"Accept": "application/json"},
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )

        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return response, CardAttributeAttachmentsModel(items=[])

        data = response.json()
        if isinstance(data, list):
            items = [CardAttributeAttachmentItemModel(**item) for item in data if isinstance(item, dict)]
        else:
            items = []
        return response, CardAttributeAttachmentsModel(items=items)
