from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_attribute_attachments.endpoints import Endpoints
from services.cards.card_attribute_attachments.models.card_attribute_attachments_model import (
    CardAttributeAttachmentItemModel,
    CardAttributeAttachmentsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardAttributeAttachmentsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /accounts/{account_id}/cards/{card_id}/attributes/attachments")
    def get_accounts_card_attribute_attachments(
        self,
        account_id: int,
        card_id: int,
    ) -> tuple[requests.Response, CardAttributeAttachmentsModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_attribute_attachments_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
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

    @allure.step("GET /accounts/{account_id}/cards/{card_id}/attributes/attachments without auth")
    def get_accounts_card_attribute_attachments_without_auth(
        self, account_id: int, card_id: int
    ) -> requests.Response:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_attribute_attachments_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
