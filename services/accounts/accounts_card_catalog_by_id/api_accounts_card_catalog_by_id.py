from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_catalog_by_id.endpoints import Endpoints
from services.accounts.accounts_card_catalog_by_id.models.accounts_card_catalog_by_id_model import (
    AccountsCardCatalogByIdListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardCatalogByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/catalog/{catalog_id}")
    def get_accounts_card_catalog_by_id(
        self,
        account_id: int,
        card_id: int,
        catalog_id: int,
    ) -> tuple[requests.Response, AccountsCardCatalogByIdListModel]:
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_catalog_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                catalog_id=int(catalog_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        return response, AccountsCardCatalogByIdListModel(items=data)

    @allure.step("GET /Accounts/{account_id}/Cards/{card_id}/catalog/{catalog_id} without auth")
    def get_accounts_card_catalog_by_id_without_auth(self, account_id: int, card_id: int, catalog_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_card_catalog_by_id_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                catalog_id=int(catalog_id),
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code}: {response.text}"
        )
        return response
