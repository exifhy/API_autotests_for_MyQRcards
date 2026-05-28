import allure
import pytest
from http import HTTPStatus

from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from services.cards.card_update.api_card_update import CardUpdateAPI
from tests.api.cards.helpers import assert_card_update_match


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards
    """
)
class TestCardsUpdateFlow:
    @allure.title("POST /Cards -> PUT /Cards/{id} -> GET /Cards/{id} -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_update_flow(self, created_card, cfg):
        created = created_card

        updated_response, payload = CardUpdateAPI().update_card(
            created.id,
            company_id=cfg["company_id_create"],
        )
        assert updated_response.status_code == HTTPStatus.ACCEPTED

        fetched = CardByIdAPI().get_card_by_id(created.id)
        assert_card_update_match(fetched, payload, card_id=created.id)
        assert fetched.cardTheme.id == payload["themeID"]

