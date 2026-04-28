import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_cards_list.api_accounts_cards_list import AccountsCardsListAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards
    """
)
class TestAccountsCardsList:
    @allure.title("POST /Cards -> GET /Accounts/{accountID}/Cards")
    def test_accounts_cards_list_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardsListAPI().get_accounts_cards(int(card.accountID))
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert any(item.id == created.id for item in model.items if item.id is not None)

    @allure.title("GET /Accounts/{accountID}/Cards supports offset/fetch query")
    def test_accounts_cards_list_with_paging_query(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, model = AccountsCardsListAPI().get_accounts_cards(
            int(card.accountID),
            offset=0,
            fetch=10,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Accounts/{accountID}/Cards without auth")
    @pytest.mark.ng
    def test_accounts_cards_list_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardsListAPI().get_accounts_cards_without_auth(int(card.accountID))
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

