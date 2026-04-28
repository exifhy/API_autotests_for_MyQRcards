import allure
import pytest
from http import HTTPStatus

from services.cards.card_designsettings_by_id.api_card_designsettings_by_id import (
    CardDesignsettingsByIdAPI,
)
from services.cards.card_designsettings_update.api_card_designsettings_update import (
    CardDesignsettingsUpdateAPI,
)
from tests.api.cards.helpers import assert_card_designsettings_match


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/designsettings
    """
)
class TestCardsDesignsettingsUpdateFlow:
    @allure.title("POST /Cards -> PUT /Cards/{id}/designsettings -> GET /Cards/{id}/designsettings -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_designsettings_update_flow(self, created_card):
        created = created_card

        updated_response, payload = CardDesignsettingsUpdateAPI().update_card_designsettings(created.id)
        assert updated_response.status_code == HTTPStatus.ACCEPTED

        fetched = CardDesignsettingsByIdAPI().get_card_designsettings_by_id(created.id)
        assert_card_designsettings_match(fetched, payload, card_id=created.id)

