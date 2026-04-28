from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_cards_list.endpoints import Endpoints
from services.cards.cards_list.models.cards_list_model import CardListItemModel, CardsListModel
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards")
    def get_accounts_cards(
        self,
        account_id: int,
        *,
        range_header: str | None = "items=0-199",
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
            url=self.endpoints.get_accounts_cards_endpoint.format(account_id=int(account_id)),
            headers=headers,
            params=params or None,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT, HTTPStatus.NO_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardsListModel(items=items)

    @allure.step("GET /Accounts/{account_id}/Cards without auth")
    def get_accounts_cards_without_auth(self, account_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_cards_endpoint.format(account_id=int(account_id)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

