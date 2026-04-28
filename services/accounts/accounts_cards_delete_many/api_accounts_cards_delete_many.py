from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_cards_delete_many.endpoints import Endpoints
from services.accounts.accounts_cards_delete_many.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardsDeleteManyAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Accounts/{account_id}/Cards/bulkremove")
    def delete_many_accounts_cards(
        self,
        account_id: int,
        card_ids: list[int] | None = None,
        *,
        payload: list[dict] | None = None,
    ):
        request_payload = payload or Payloads.build_accounts_cards_delete_many_payload(
            account_id=int(account_id),
            card_ids=card_ids or [],
        )
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_many_accounts_cards_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, request_payload

