import allure
import pytest

from services.cardlinks.cardlink_card.api_cardlink_card import CardLinkCardAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardLinks/{cardLink}/card
    """
)
class TestCardLinksCard:
    @allure.title("POST /Cards -> GET /cardLinks/{cardLink}/card -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_card_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        fetched = CardLinkCardAPI().get_cardlink_card(card_link_id)
        assert fetched.id == created.id
        assert fetched.accountID is not None
        assert fetched.person is not None
        assert fetched.url is None or fetched.url != ""
