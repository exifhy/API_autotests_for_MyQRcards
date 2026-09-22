from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_attributes_list_v2.endpoints import Endpoints
from services.cards.card_attributes_list_v2.models.card_attributes_list_v2_model import (
    CardAttributeNodeV2Model,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardAttributesListV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/cards/{card_id}/attributes/V2")
    def get_accounts_card_attributes_v2(self, account_id: int, card_id: int) -> list[CardAttributeNodeV2Model]:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_attributes_v2_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected 200/204, got {response.status_code}: {response.text}"
        )
        if response.status_code == HTTPStatus.NO_CONTENT or not response.text:
            return []
        return [CardAttributeNodeV2Model(**item) for item in response.json()]

    @allure.step("GET /Accounts/{account_id}/cards/{card_id}/attributes/V2 (without auth)")
    def get_accounts_card_attributes_v2_without_auth(self, account_id: int, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_attributes_v2_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
