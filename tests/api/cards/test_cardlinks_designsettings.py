import allure
import pytest

from services.cardlinks.cardlink_designsettings.api_cardlink_designsettings import (
    CardLinkDesignsettingsAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardLinks/{cardLink}/designsettings
    """
)
class TestCardLinksDesignsettings:
    @allure.title("POST /Cards -> GET /cardLinks/{cardLink}/designsettings -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_designsettings_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        model = CardLinkDesignsettingsAPI().get_cardlink_designsettings(card_link_id)
        assert model.cardID == created.id
        assert model.accountID is not None
