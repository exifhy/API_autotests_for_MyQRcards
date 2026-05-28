import allure
import pytest
from http import HTTPStatus

from services.cardlinks.cardlinks_list.api_cardlinks_list import CardLinksListAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.cards_list.api_cards_list import CardsListAPI
from tests.api.cards.helpers import extract_account_uri_name


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardLinks?accountUriName=...
    """
)
class TestCardLinksList:
    @allure.title("GET /Cards -> GET /cardLinks?accountUriName=...")
    @pytest.mark.smoke
    def test_cardlinks_list_flow(self):
        _, cards = CardsListAPI().get_cards(range_header=None, offset=0, fetch=20)
        assert cards.items, "Cards list is empty"

        source_card_id = next((item.id for item in cards.items if item.id is not None), None)
        assert source_card_id is not None, "No card id found in cards list"

        card = CardByIdAPI().get_card_by_id(source_card_id)
        assert card.accountUrl, "Card accountUrl is empty"
        account_uri_name = extract_account_uri_name(card.accountUrl)
        assert account_uri_name, "accountUriName is empty"

        response, model = CardLinksListAPI().get_cardlinks(account_uri_name=account_uri_name)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(model.items, list)
        assert model.items, "Expected non-empty cardLinks list"
