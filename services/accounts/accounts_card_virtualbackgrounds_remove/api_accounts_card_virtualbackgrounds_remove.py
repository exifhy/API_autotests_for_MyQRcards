from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_virtualbackgrounds_remove.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardVirtualBackgroundsRemoveAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Accounts/{account_id}/Cards/{card_id}/virtualbackground")
    def remove_accounts_card_virtualbackgrounds(self, account_id: int, card_id: int, background_ids: list[int]):
        response = self._call(
            "DELETE",
            url=self.endpoints.accounts_card_virtualbackgrounds_remove_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=background_ids,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response
