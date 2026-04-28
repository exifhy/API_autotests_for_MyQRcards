from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_card_catalog_items_update.endpoints import Endpoints
from services.accounts.accounts_card_catalog_items_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCardCatalogItemsUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Accounts/{account_id}/Cards/{card_id}/catalog/{catalog_id}")
    def update_accounts_card_catalog_items(
        self,
        account_id: int,
        card_id: int,
        catalog_id: int,
        *,
        item_id: int | None = None,
        name: str | None = None,
        payload: list[dict] | None = None,
    ):
        request_payload = payload or Payloads.build_accounts_card_catalog_items_update_payload(
            item_id=int(item_id),
            name=name or "Catalog item updated",
        )
        response = self._call(
            "PUT",
            url=self.endpoints.update_accounts_card_catalog_items_endpoint.format(
                account_id=int(account_id),
                card_id=int(card_id),
                catalog_id=int(catalog_id),
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code == HTTPStatus.ACCEPTED, (
            f"Expected HTTPStatus.ACCEPTED, got {response.status_code}: {response.text}"
        )
        return response, request_payload

