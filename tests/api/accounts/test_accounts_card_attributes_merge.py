import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_attributes_list.api_accounts_card_attributes_list import (
    AccountsCardAttributesListAPI,
)
from services.accounts.accounts_card_attributes_merge.api_accounts_card_attributes_merge import (
    AccountsCardAttributesMergeAPI,
)
from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@allure.description(
    """
    PUT /accounts/{id}/cards/{cardId}/attributes
    """
)
class TestAccountsCardAttributesMerge:
    @allure.title("POST card -> PUT /accounts/{id}/cards/{cardId}/attributes -> GET verify -> DELETE")
    def test_accounts_card_attributes_merge_200(self, cfg):
        card_id = None
        try:
            with allure.step("POST — create card"):
                _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
                card_id = int(created.id)

            with allure.step(f"PUT /accounts/{cfg['lk_account_id']}/cards/{card_id}/attributes"):
                response = AccountsCardAttributesMergeAPI().merge_accounts_card_attributes(
                    int(cfg["lk_account_id"]),
                    card_id,
                )
                assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

            with allure.step(f"GET /accounts/{cfg['lk_account_id']}/cards/{card_id}/attributes/"):
                _, model = AccountsCardAttributesListAPI().get_accounts_card_attributes(
                    int(cfg["lk_account_id"]),
                    card_id,
                )
                assert isinstance(model.items, list)

        finally:
            if card_id is not None:
                try:
                    CardDeleteByIdAPI().delete_card_by_id(card_id)
                except Exception:
                    pass

    @pytest.mark.ng
    @allure.title("PUT /accounts/{id}/cards/{cardId}/attributes without auth -> 401/403")
    def test_accounts_card_attributes_merge_401_without_auth(self, cfg):
        response = AccountsCardAttributesMergeAPI().merge_accounts_card_attributes_without_auth(
            account_id=int(cfg["lk_account_id"]),
            card_id=1,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
