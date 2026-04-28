from http import HTTPStatus

import allure

from config.headers import Headers
from services.cards.card_attachments_sortorder.endpoints import Endpoints
from services.cards.card_attachments_sortorder.models.card_attachments_sortorder_model import (
    CardAttachmentsSortOrderResponseModel,
    CardAttachmentSortOrderItemModel,
)
from services.cards.card_attachments_sortorder.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttachmentsSortOrderAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Cards/{card_id}/attachments/sortorder")
    def get_card_attachments_sortorder(self, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.card_attachments_sortorder_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        if isinstance(data, dict) and "attachmentSortOrder" in data:
            model = CardAttachmentsSortOrderResponseModel(**data)
            return response, model.attachmentSortOrder
        if isinstance(data, list):
            return response, [CardAttachmentSortOrderItemModel(**item) for item in data]
        return response, []

    @allure.step("PUT /Cards/{card_id}/attachments/sortorder")
    def update_card_attachments_sortorder(self, card_id: int, *items: dict):
        payload = Payloads.build_card_attachments_sortorder_payload(*items)
        response = self._call(
            "PUT",
            url=self.endpoints.card_attachments_sortorder_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, payload
