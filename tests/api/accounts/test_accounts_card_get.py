import allure
import pytest
from http import HTTPStatus

from services.accounts.accounts_card_by_id.api_accounts_card_by_id import AccountsCardByIdAPI
from services.accounts.accounts_card_by_id_v2.api_accounts_card_by_id_v2 import AccountsCardByIdV2API
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import assert_card_basic, assert_card_full


@allure.epic("API")
@allure.feature("Accounts")
@pytest.mark.api
@pytest.mark.accounts
@allure.description(
    """
    /Accounts/{accountID}/Cards/{cardID}
    /Accounts/{accountID}/Cards/{cardID}/V2
    """
)
class TestAccountsCardGet:
    @allure.title("POST /Cards -> GET /Accounts/{accountID}/Cards/{cardID}")
    @pytest.mark.smoke
    def test_accounts_card_get_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        fetched = AccountsCardByIdAPI().get_accounts_card_by_id(int(card.accountID), int(created.id))
        assert_card_basic(fetched, card_id=created.id)
        assert fetched.accountID == card.accountID

    @allure.title("POST /Cards -> GET /Accounts/{accountID}/Cards/{cardID}/V2")
    def test_accounts_card_get_v2_flow(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response, fetched = AccountsCardByIdV2API().get_accounts_card_by_id_v2(int(card.accountID), int(created.id))
        assert response.status_code == HTTPStatus.OK
        assert_card_full(fetched, card_id=created.id)
        assert fetched.accountID == card.accountID

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID} without auth")
    @pytest.mark.ng
    def test_accounts_card_get_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardByIdAPI().get_accounts_card_by_id_without_auth(int(card.accountID), int(created.id))
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

    @allure.title("GET /Accounts/{accountID}/Cards/{cardID}/V2 without auth")
    @pytest.mark.ng
    def test_accounts_card_get_v2_without_auth(self, created_card):
        created = created_card
        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.accountID is not None, "Card accountID is empty"

        response = AccountsCardByIdV2API().get_accounts_card_by_id_v2_without_auth(
            int(card.accountID),
            int(created.id),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
