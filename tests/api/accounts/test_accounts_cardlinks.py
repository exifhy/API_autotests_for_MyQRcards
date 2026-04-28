import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cardlinks_list.api_accounts_cardlinks_list import AccountsCardLinksListAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/links
    """
)
class TestAccountsCardLinks:
    @allure.title("POST /Cards -> GET /Accounts/{accountID}/Cards/links")
    def test_accounts_cardlinks_list_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardLinksListAPI().get_accounts_cardlinks(int(card.accountID))
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.PARTIAL_CONTENT)
        assert any(
            (
                item.cardID == created.id
                or (item.card is not None and item.card.id == created.id)
            )
            for item in model.items
        )
        assert any(
            (
                item.accountID == card.accountID
                or (item.account is not None and item.account.id == card.accountID)
            )
            for item in model.items
        )

    @allure.title("GET /Accounts/{accountID}/Cards/links without auth")
    @pytest.mark.ng
    def test_accounts_cardlinks_list_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardLinksListAPI().get_accounts_cardlinks_without_auth(int(card.accountID))
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
