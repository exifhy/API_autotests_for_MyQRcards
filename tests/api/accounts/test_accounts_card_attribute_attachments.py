import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_attribute_attachments.api_accounts_card_attribute_attachments import (
    AccountsCardAttributeAttachmentsAPI,
)
from services.accounts.accounts_card_create.api_accounts_card_create import AccountsCardCreateAPI
from services.cards.card_delete_by_id.api_card_delete_by_id import CardDeleteByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@allure.description(
    """
    GET /accounts/{id}/cards/{cardId}/attributes/attachments
    """
)
class TestAccountsCardAttributeAttachments:
    @allure.title("POST card -> GET /accounts/{id}/cards/{cardId}/attributes/attachments -> DELETE")
    @pytest.mark.smoke
    def test_accounts_card_attribute_attachments_200(self, cfg):
        card_id = None
        try:
            with allure.step("POST — create card"):
                _, created, _ = AccountsCardCreateAPI().create_accounts_card(int(cfg["lk_account_id"]))
                card_id = int(created.id)

            with allure.step(f"GET /accounts/{cfg['lk_account_id']}/cards/{card_id}/attributes/attachments"):
                response, model = AccountsCardAttributeAttachmentsAPI().get_accounts_card_attribute_attachments(
                    int(cfg["lk_account_id"]),
                    card_id,
                )

            assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT)
            assert isinstance(model.items, list)

        finally:
            if card_id is not None:
                try:
                    CardDeleteByIdAPI().delete_card_by_id(card_id)
                except Exception:
                    pass

    @pytest.mark.ng
    @allure.title("GET /accounts/{id}/cards/{cardId}/attributes/attachments without auth -> 401/403")
    def test_accounts_card_attribute_attachments_401_without_auth(self, cfg):
        response = AccountsCardAttributeAttachmentsAPI().get_accounts_card_attribute_attachments_without_auth(
            account_id=int(cfg["lk_account_id"]),
            card_id=1,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
