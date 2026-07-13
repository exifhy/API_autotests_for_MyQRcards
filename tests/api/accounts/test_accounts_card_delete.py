import time
from http import HTTPStatus

import allure
import pytest

from config.headers import Headers
from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.accounts.accounts_card_delete_by_id.api_accounts_card_delete_by_id import AccountsCardDeleteByIdAPI
from services.accounts.accounts_cards_delete_many.api_accounts_cards_delete_many import AccountsCardsDeleteManyAPI
from src.support.helper import Helper
from src.support.token_utils import get_token
from src.support.waiter import wait_until

_helper = Helper()


def _wait_card_absent(host: str, card_id: int, timeout_s: int = 120, step_s: int = 5):
    headers = Headers.auth_header(bearer_token=get_token())

    def _gone():
        response = _helper._call(
            "GET",
            url=f"{host}/Cards/{int(card_id)}",
            headers=headers,
        )
        if response.status_code in (HTTPStatus.NO_CONTENT, HTTPStatus.NOT_FOUND, HTTPStatus.CONFLICT):
            return True
        return None

    return wait_until(_gone, timeout_s=timeout_s, step_s=step_s)


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}
    /Accounts/{accountID}/Cards/bulkremove
    """
)
class TestAccountsCardDelete:
    @allure.title("POST /Accounts/{accountID}/Cards -> DELETE /Accounts/{accountID}/Cards/{cardID}")
    def test_accounts_card_delete_by_id_flow(self, cfg):
        created_id = None
        try:
            _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
            assert created.id is not None
            created_id = int(created.id)

            deleted = AccountsCardDeleteByIdAPI().delete_accounts_card_by_id(int(cfg["lk_account_id"]), created_id)
            assert deleted.status_code == HTTPStatus.ACCEPTED

            host = str(cfg["host"]).rstrip("/")
            is_absent = _wait_card_absent(host, created_id)
            assert is_absent is True, f"Card {created_id} is still available after delete"
            created_id = None
        finally:
            if created_id is not None:
                try:
                    headers = Headers.auth_header(bearer_token=get_token())
                    host = str(cfg["host"]).rstrip("/")
                    _helper._call("DELETE", url=f"{host}/Cards/{int(created_id)}", headers=headers)
                except Exception:
                    pass

    @allure.title("POST multiple /Accounts/{accountID}/Cards -> DELETE /Accounts/{accountID}/Cards/bulkremove")
    def test_accounts_cards_delete_many_flow(self, cfg):
        created_ids: list[int] = []
        try:
            for _ in range(3):
                _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
                assert created.id is not None
                created_ids.append(int(created.id))

            response, payload = AccountsCardsDeleteManyAPI().delete_many_accounts_cards(
                int(cfg["lk_account_id"]),
                created_ids,
            )
            assert response.status_code == HTTPStatus.ACCEPTED
            assert len(payload) == len(created_ids)

            host = str(cfg["host"]).rstrip("/")
            for card_id in created_ids:
                is_absent = _wait_card_absent(host, card_id)
                assert is_absent is True, f"Card {card_id} is still available after bulk delete"
        finally:
            headers = Headers.auth_header(bearer_token=get_token())
            host = str(cfg["host"]).rstrip("/")
            for card_id in created_ids:
                try:
                    _helper._call("DELETE", url=f"{host}/Cards/{int(card_id)}", headers=headers)
                except Exception:
                    pass
