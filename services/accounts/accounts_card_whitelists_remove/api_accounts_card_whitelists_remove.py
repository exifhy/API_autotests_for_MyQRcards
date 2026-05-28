from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_whitelists_remove.endpoints import Endpoints
from services.accounts.accounts_card_whitelists_remove.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardWhitelistsRemoveAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Accounts/{account_id}/Cards/{card_id}/whiteLists")
    def remove_accounts_card_whitelists(
        self,
        account_id: int,
        card_id: int,
        allowed_account_ids: list[int] | None = None,
        *,
        payload: list[int] | None = None,
    ):
        request_payload = payload or Payloads.build_accounts_card_whitelists_remove_payload(allowed_account_ids or [])
        response = self._call(
            "DELETE",
            url=self.endpoints.remove_accounts_card_whitelists_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, request_payload

