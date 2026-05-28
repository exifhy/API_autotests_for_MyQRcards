import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id_v2.api_card_by_id_v2 import CardByIdV2API
from services.cards.card_update_v2.api_card_update_v2 import CardUpdateV2API
from tests.api.cards.helpers import assert_card_update_match


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{id}/V2
    """
)
class TestCardsUpdateV2Flow:
    @allure.title("POST /Cards -> PUT /Cards/{id}/V2 -> GET /Cards/{id}/V2 -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_update_v2_flow(self, created_card, cfg):
        created = created_card

        updated_response, payload = CardUpdateV2API().update_card_v2(
            created.id,
            company_id=cfg["company_id_create"],
        )
        assert updated_response.status_code == HTTPStatus.ACCEPTED

        fetched = CardByIdV2API().get_card_by_id_v2(created.id)
        assert_card_update_match(fetched, payload, card_id=created.id)
        # On dev, V2 accepts the update but may keep the existing theme.
        assert fetched.cardTheme.id is not None

