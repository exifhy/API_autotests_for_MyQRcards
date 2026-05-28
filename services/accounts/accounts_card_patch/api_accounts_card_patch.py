from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_patch.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardPatchAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PATCH /Accounts/{account_id}/Cards/{card_id}")
    def patch_accounts_card(self, account_id: int, card_id: int, body):
        response = self._call(
            "PATCH",
            url=self.endpoints.patch_accounts_card_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=body,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response

