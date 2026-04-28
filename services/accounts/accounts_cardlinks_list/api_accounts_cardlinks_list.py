from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_cardlinks_list.endpoints import Endpoints
from services.cardlinks.cardlinks_list.models.cardlinks_list_model import (
    CardLinksListItemModel,
    CardLinksListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardLinksListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/links")
    def get_accounts_cardlinks(self, account_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_cardlinks_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT, HTTPStatus.NO_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got: {type(data)} / {data}"
        items = [CardLinksListItemModel(**item) for item in data if isinstance(item, dict)]
        return response, CardLinksListModel(items=items)

    @allure.step("GET /Accounts/{account_id}/Cards/links without auth")
    def get_accounts_cardlinks_without_auth(self, account_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_cardlinks_endpoint.format(account_id=int(account_id)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response

