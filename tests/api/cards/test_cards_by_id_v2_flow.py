import allure
import pytest

from services.cards.card_by_id_v2.api_card_by_id_v2 import CardByIdV2API
from tests.api.cards.helpers import assert_card_full


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{id}/V2
    """
)
class TestCardsByIdV2:
    @allure.title("POST /Cards -> GET /Cards/{id}/V2 -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_get_by_id_v2_flow(self, created_card):
        created = created_card

        fetched = CardByIdV2API().get_card_by_id_v2(created.id)
        assert_card_full(fetched, card_id=created.id)

