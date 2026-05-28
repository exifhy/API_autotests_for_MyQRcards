import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_whitelists_add.api_accounts_card_whitelists_add import (
    AccountsCardWhitelistsAddAPI,
)
from services.accounts.accounts_card_whitelists.api_accounts_card_whitelists import AccountsCardWhitelistsAPI
from services.accounts.accounts_card_whitelists_remove.api_accounts_card_whitelists_remove import (
    AccountsCardWhitelistsRemoveAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}/whiteLists
    """
)
class TestAccountsCardWhitelists:
    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/whiteLists")
    def test_accounts_card_whitelists_list_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardWhitelistsAPI().get_accounts_card_whitelists(
            int(card.accountID),
            int(created.id),
        )
        assert response.status_code == HTTPStatus.OK
        assert isinstance(model.items, list)
        assert all(item.cardID in (None, created.id) for item in model.items)
        assert all(item.accountID in (None, card.accountID) for item in model.items)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/whiteLists supports Range/offset/fetch")
    def test_accounts_card_whitelists_paging_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardWhitelistsAPI().get_accounts_card_whitelists(
            int(card.accountID),
            int(created.id),
            range_header="items=0-49",
            offset=0,
            fetch=10,
        )
        assert response.status_code == HTTPStatus.PARTIAL_CONTENT
        assert isinstance(model.items, list)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/whiteLists without auth")
    @pytest.mark.ng
    def test_accounts_card_whitelists_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardWhitelistsAPI().get_accounts_card_whitelists_without_auth(
            int(card.accountID),
            int(created.id),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

    @allure.title("POST whiteList -> GET whiteLists -> DELETE whiteList -> GET whiteLists")
    def test_accounts_card_whitelists_add_remove_flow(self, created_card, cfg):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        allowed_account_id = int(cfg["mobile_account_id"])

        add_response, add_payload = AccountsCardWhitelistsAddAPI().add_accounts_card_whitelists(
            int(card.accountID),
            int(created.id),
            [allowed_account_id],
        )
        assert add_response.status_code == HTTPStatus.OK
        assert add_payload == [allowed_account_id]

        list_response, list_model = AccountsCardWhitelistsAPI().get_accounts_card_whitelists(
            int(card.accountID),
            int(created.id),
        )
        assert list_response.status_code == HTTPStatus.OK
        assert any(item.allowedAccountID == allowed_account_id for item in list_model.items)

        remove_response, remove_payload = AccountsCardWhitelistsRemoveAPI().remove_accounts_card_whitelists(
            int(card.accountID),
            int(created.id),
            [allowed_account_id],
        )
        assert remove_response.status_code == HTTPStatus.ACCEPTED
        assert remove_payload == [allowed_account_id]

        response_after_remove, model_after_remove = AccountsCardWhitelistsAPI().get_accounts_card_whitelists(
            int(card.accountID),
            int(created.id),
        )
        assert response_after_remove.status_code == HTTPStatus.OK
        assert all(item.allowedAccountID != allowed_account_id for item in model_after_remove.items)
