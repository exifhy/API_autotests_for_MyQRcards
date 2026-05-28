from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_whitelists.endpoints import Endpoints
from services.accounts.accounts_card_whitelists.models.accounts_card_whitelists_model import (
    AccountsCardWhitelistItemModel,
    AccountsCardWhitelistsModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardWhitelistsAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/whiteLists")
    def get_accounts_card_whitelists(
        self,
        account_id: int,
        card_id: int,
        *,
        range_header: str | None = None,
        offset: int | None = None,
        fetch: int | None = None,
    ):
        params: dict[str, str] = {}
        if offset is not None:
            params["offset"] = str(offset)
        if fetch is not None:
            params["fetch"] = str(fetch)

        headers = Headers.auth_header(bearer_token=get_token())
        if range_header:
            headers["Range"] = range_header

        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_whitelists_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [AccountsCardWhitelistItemModel(**item) for item in data if isinstance(item, dict)]
        return response, AccountsCardWhitelistsModel(items=items)

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/whiteLists without auth")
    def get_accounts_card_whitelists_without_auth(self, account_id: int, card_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_whitelists_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

