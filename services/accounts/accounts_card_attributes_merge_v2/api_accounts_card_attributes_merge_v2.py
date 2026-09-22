from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_attributes_merge_v2.endpoints import Endpoints
from services.cards.card_attributes_merge_v2.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardAttributesMergeV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Accounts/{account_id}/cards/{card_id}/attributes/V2")
    def merge_accounts_card_attributes_v2(self, account_id: int, card_id: int, *, payload: list[dict] | None = None):
        request_payload = payload if payload is not None else Payloads.build_card_attributes_v2_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.merge_accounts_card_attributes_v2_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected 200/202/204, got {response.status_code}: {response.text}"
        )
        return response

    @allure.step("PUT /Accounts/{account_id}/cards/{card_id}/attributes/V2 (without auth)")
    def merge_accounts_card_attributes_v2_without_auth(self, account_id: int, card_id: int):
        response = self._call(
            "PUT",
            url=self.endpoints.merge_accounts_card_attributes_v2_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.without_authorization_field_header(),
            json=Payloads.build_card_attributes_v2_payload(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
