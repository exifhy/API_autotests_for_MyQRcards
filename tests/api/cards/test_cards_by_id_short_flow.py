import allure
import pytest

from services.cards.card_by_id_short.api_card_by_id_short import CardByIdShortAPI
from tests.api.cards.helpers import assert_card_basic


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{id}/short
    """
)
class TestCardsByIdShort:
    @allure.title("POST /Cards -> GET /Cards/{id}/short -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_get_by_id_short_flow(self, created_card):
        created = created_card

        fetched = CardByIdShortAPI().get_card_by_id_short(created.id)
        assert_card_basic(fetched, card_id=created.id)
        assert fetched.company is not None
        assert fetched.company.id is not None
        assert fetched.cardLinkUrl is None or fetched.cardLinkUrl != ''

