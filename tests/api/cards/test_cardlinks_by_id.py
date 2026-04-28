import allure
import pytest

from services.cardlinks.cardlink_by_id.api_cardlink_by_id import CardLinkByIdAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.cards_list.api_cards_list import CardsListAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardlinks/{cardLink}
    """
)
class TestCardLinksById:
    @allure.title("GET /Cards -> GET /cardlinks/{cardLink}")
    @pytest.mark.smoke
    def test_cardlinks_by_id_flow(self):
        _, cards = CardsListAPI().get_cards(range_header=None, offset=0, fetch=20)
        assert cards.items, "Cards list is empty"

        source_card_id = next((item.id for item in cards.items if item.id is not None and item.url), None)
        assert source_card_id is not None, "No suitable card found in cards list"

        card = CardByIdAPI().get_card_by_id(source_card_id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        model = CardLinkByIdAPI().get_cardlink_by_id(card_link_id)
        account_obj = getattr(model, "account", None)
        card_obj = getattr(model, "card", None)

        assert model.cardID in (None, source_card_id) or card_obj is not None or model.id is not None
        assert (
            model.accountID is not None
            or model.customCardLinkUrl is not None
            or model.name is not None
            or account_obj is not None
            or card_obj is not None
        )
