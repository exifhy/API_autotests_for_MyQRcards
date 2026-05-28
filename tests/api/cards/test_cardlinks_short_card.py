import allure
import pytest

from services.cardlinks.cardlink_short_card.api_cardlink_short_card import CardLinkShortCardAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardLinks/{cardLink}/short/card
    """
)
class TestCardLinksShortCard:
    @allure.title("POST /Cards -> GET /cardLinks/{cardLink}/short/card -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_short_card_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        fetched = CardLinkShortCardAPI().get_cardlink_short_card(card_link_id)
        assert fetched.id == created.id
        assert fetched.person is not None
        assert fetched.company is not None
        assert fetched.company.id is not None
        assert fetched.cardLinkUrl is None or fetched.cardLinkUrl != ""
