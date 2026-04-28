from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.accounts.accounts_card_catalog_items_create.endpoints import Endpoints
from services.accounts.accounts_card_catalog_items_create.models.accounts_card_catalog_items_create_model import (
    AccountsCardCatalogItemsCreateModel,
)
from services.accounts.accounts_card_catalog_items_create.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardCatalogItemsCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/{account_id}/Cards/{card_id}/catalog/{catalog_id}")
    def create_accounts_card_catalog_items(
        self,
        account_id: int,
        card_id: int,
        catalog_id: int,
        *,
        name: str | None = None,
        payload: list[dict] | None = None,
    ) -> tuple[requests.Response, AccountsCardCatalogItemsCreateModel, list[dict]]:
        request_payload = payload or Payloads.build_accounts_card_catalog_items_create_payload(
            name=name or "Catalog item autotest",
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_accounts_card_catalog_items_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                catalog_id=int(catalog_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        return response, AccountsCardCatalogItemsCreateModel(items=data), request_payload

