import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_by_id.api_accounts_card_by_id import AccountsCardByIdAPI
from services.accounts.accounts_card_by_id_v2.api_accounts_card_by_id_v2 import AccountsCardByIdV2API
from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.accounts.accounts_card_create_v2.api_accounts_card_create_v2 import AccountsCardCreateV2API
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards
    /Accounts/{accountID}/Cards/V2
    """
)
class TestAccountsCardCreate:
    @allure.title("POST /Accounts/{accountID}/Cards -> GET /Accounts/{accountID}/Cards/{cardID} -> DELETE /Cards/{id}")
    def test_accounts_card_create_minimal_flow(self, cfg):
        created_id = None
        try:
            response, created, payload = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
            assert response.status_code == HTTPStatus.CREATED
            assert created.id is not None
            created_id = int(created.id)

            fetched = AccountsCardByIdAPI().get_accounts_card_by_id(int(cfg["lk_account_id"]), created_id)
            assert fetched.id == created_id
            assert fetched.name == payload["Name"]
            assert fetched.person is not None
            assert fetched.person.firstName == payload["Person"]["FirstName"]
        finally:
            if created_id is not None:
                CardDeleteByIdAPI().delete_card_by_id(created_id)

    @allure.title("POST /Accounts/{accountID}/Cards/V2 -> GET /Accounts/{accountID}/Cards/{cardID}/V2 -> DELETE /Cards/{id}")
    def test_accounts_card_create_v2_minimal_flow(self, cfg):
        created_id = None
        try:
            response, created, payload = AccountsCardCreateV2API().create_accounts_card_v2(int(cfg["lk_account_id"]))
            assert response.status_code == HTTPStatus.CREATED
            assert created.id is not None
            created_id = int(created.id)

            get_response, fetched = AccountsCardByIdV2API().get_accounts_card_by_id_v2(int(cfg["lk_account_id"]), created_id)
            assert get_response.status_code == HTTPStatus.OK
            assert fetched.id == created_id
            assert fetched.name == payload["Name"]
            assert fetched.person is not None
            assert fetched.person.firstName == payload["Person"]["FirstName"]
        finally:
            if created_id is not None:
                CardDeleteByIdAPI().delete_card_by_id(created_id)
