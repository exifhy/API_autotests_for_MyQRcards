import time
from http import HTTPStatus

import allure
import pytest

from config.headers import Headers
from services.accounts.accounts_card_catalog_by_id.api_accounts_card_catalog_by_id import (
    AccountsCardCatalogByIdAPI,
)
from services.accounts.accounts_card_catalog_create.api_accounts_card_catalog_create import (
    AccountsCardCatalogCreateAPI,
)
from services.accounts.accounts_card_catalog_delete.api_accounts_card_catalog_delete import (
    AccountsCardCatalogDeleteAPI,
)
from services.accounts.accounts_card_catalog_items_create.api_accounts_card_catalog_items_create import (
    AccountsCardCatalogItemsCreateAPI,
)
from services.accounts.accounts_card_catalog_items_delete.api_accounts_card_catalog_items_delete import (
    AccountsCardCatalogItemsDeleteAPI,
)
from services.accounts.accounts_card_catalog_items_update.api_accounts_card_catalog_items_update import (
    AccountsCardCatalogItemsUpdateAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from src.support.helper import Helper
from src.support.token_utils import get_token
from src.support.waiter import wait_until

_helper = Helper()


def _wait_catalog_absent(host: str, account_id: int, card_id: int, catalog_id: int, timeout_s: int = 30, step_s: int = 2):
    headers = Headers.auth_header(bearer_token=get_token())

    def _gone():
        response = _helper._call(
            "GET",
            url=f"{host}/accounts/{int(account_id)}/cards/{int(card_id)}/catalog/{int(catalog_id)}",
            headers=headers,
        )
        if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT):
            return True
        if response.status_code == HTTPStatus.OK and not response.text:
            return True
        return None

    return wait_until(_gone, timeout_s=timeout_s, step_s=step_s)


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}/catalog
    /Accounts/{accountID}/Cards/{cardID}/catalog/{catalogID}
    """
)
class TestAccountsCardCatalog:
    @allure.title("POST catalog -> GET by id -> DELETE catalog")
    def test_accounts_card_catalog_crud_flow(self, created_card, cfg):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        catalog_name = f"Catalog_{int(time.time())}"
        create_response, created_model, payload = AccountsCardCatalogCreateAPI().create_accounts_card_catalog(
            int(card.accountID),
            int(created.id),
            name=catalog_name,
        )
        assert create_response.status_code == HTTPStatus.OK
        assert created_model.items, "Catalog create returned empty items"
        assert created_model.items[0].id is not None, "Catalog create returned empty id"
        catalog_id = int(created_model.items[0].id)

        get_response, get_model = AccountsCardCatalogByIdAPI().get_accounts_card_catalog_by_id(
            int(card.accountID),
            int(created.id),
            catalog_id,
        )
        assert get_response.status_code == HTTPStatus.OK
        assert get_model.items, "Catalog get returned empty items"
        fetched = get_model.items[0]
        assert int(getattr(fetched, "catalogID", 0)) == catalog_id
        assert int(getattr(fetched, "cardID", 0)) == int(created.id)
        assert str(getattr(fetched, "name", "") or "") == payload[0]["name"]

        deleted = AccountsCardCatalogDeleteAPI().delete_accounts_card_catalog(
            int(card.accountID),
            int(created.id),
            [catalog_id],
        )
        assert deleted.status_code == HTTPStatus.ACCEPTED

        host = str(cfg["host"]).rstrip("/")
        is_absent = _wait_catalog_absent(host, int(card.accountID), int(created.id), catalog_id)
        assert is_absent is True, "Catalog is still available after delete"

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/catalog/{catalogID} without auth")
    @pytest.mark.ng
    def test_accounts_card_catalog_by_id_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        _, created_model, _ = AccountsCardCatalogCreateAPI().create_accounts_card_catalog(
            int(card.accountID),
            int(created.id),
            name=f"Catalog_{int(time.time())}",
        )
        assert created_model.items and created_model.items[0].id is not None
        catalog_id = int(created_model.items[0].id)

        response = AccountsCardCatalogByIdAPI().get_accounts_card_catalog_by_id_without_auth(
            int(card.accountID),
            int(created.id),
            catalog_id,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

    @allure.title("POST catalog -> POST item -> PUT item -> DELETE catalog cascades item delete")
    def test_accounts_card_catalog_item_cascade_flow(self, created_card, cfg):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        _, created_catalog_model, _ = AccountsCardCatalogCreateAPI().create_accounts_card_catalog(
            int(card.accountID),
            int(created.id),
            name=f"Catalog_{int(time.time())}",
        )
        assert created_catalog_model.items and created_catalog_model.items[0].id is not None
        catalog_id = int(created_catalog_model.items[0].id)

        item_name = f"Item_{int(time.time())}"
        _, created_item_model, _ = AccountsCardCatalogItemsCreateAPI().create_accounts_card_catalog_items(
            int(card.accountID),
            int(created.id),
            catalog_id,
            name=item_name,
        )
        assert created_item_model.items and created_item_model.items[0].id is not None
        item_id = int(created_item_model.items[0].id)

        updated_name = f"{item_name}_updated"
        update_response, update_payload = AccountsCardCatalogItemsUpdateAPI().update_accounts_card_catalog_items(
            int(card.accountID),
            int(created.id),
            catalog_id,
            item_id=item_id,
            name=updated_name,
        )
        assert update_response.status_code == HTTPStatus.ACCEPTED

        get_response, get_model = AccountsCardCatalogByIdAPI().get_accounts_card_catalog_by_id(
            int(card.accountID),
            int(created.id),
            catalog_id,
        )
        assert get_response.status_code == HTTPStatus.OK
        assert any(int(getattr(item, "id", 0) or 0) == item_id for item in get_model.items)
        matched = next(
            (item for item in get_model.items if int(getattr(item, "id", 0) or 0) == item_id),
            None,
        )
        assert matched is not None, "Catalog item not found after update"
        assert str(getattr(matched, "name", "") or "") == update_payload[0]["name"]

        deleted = AccountsCardCatalogDeleteAPI().delete_accounts_card_catalog(
            int(card.accountID),
            int(created.id),
            [catalog_id],
        )
        assert deleted.status_code == HTTPStatus.ACCEPTED

        host = str(cfg["host"]).rstrip("/")
        is_absent = _wait_catalog_absent(host, int(card.accountID), int(created.id), catalog_id)
        assert is_absent is True, "Catalog is still available after delete"

    @allure.title("POST catalog -> POST item -> DELETE item -> GET catalog (item absent)")
    def test_accounts_card_catalog_item_delete_flow(self, created_card):
        catalog_id = None
        card = CardByIdAPI().get_card_by_id(created_card.id)
        assert card.accountID is not None, "Card accountID is empty"
        account_id = int(card.accountID)
        card_id = int(created_card.id)
        try:
            with allure.step("POST — create catalog"):
                _, catalog_model, _ = AccountsCardCatalogCreateAPI().create_accounts_card_catalog(
                    account_id, card_id, name=f"Catalog_{int(time.time())}",
                )
                assert catalog_model.items and catalog_model.items[0].id is not None
                catalog_id = int(catalog_model.items[0].id)

            with allure.step("POST — create item in catalog"):
                _, item_model, _ = AccountsCardCatalogItemsCreateAPI().create_accounts_card_catalog_items(
                    account_id, card_id, catalog_id, name=f"Item_{int(time.time())}",
                )
                assert item_model.items and item_model.items[0].id is not None
                item_id = int(item_model.items[0].id)

            with allure.step(f"DELETE catalog item id={item_id}"):
                delete_response = AccountsCardCatalogItemsDeleteAPI().delete_accounts_card_catalog_items(
                    account_id, card_id, catalog_id, [item_id],
                )
                assert delete_response.status_code == HTTPStatus.ACCEPTED

            with allure.step("GET catalog — verify item is gone"):
                get_response, get_model = AccountsCardCatalogByIdAPI().get_accounts_card_catalog_by_id(
                    account_id, card_id, catalog_id,
                )
                assert get_response.status_code == HTTPStatus.OK
                remaining_ids = [int(getattr(i, "id", 0) or 0) for i in get_model.items]
                assert item_id not in remaining_ids, f"Item {item_id} still present after DELETE"

        finally:
            if catalog_id is not None:
                try:
                    AccountsCardCatalogDeleteAPI().delete_accounts_card_catalog(
                        account_id, card_id, [catalog_id],
                    )
                except Exception:
                    pass
