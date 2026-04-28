import allure
import pytest
from http import HTTPStatus

from services.cards.card_designsettings_by_id.api_card_designsettings_by_id import (
    CardDesignsettingsByIdAPI,
)


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{cardID}/designSettings
    """
)
class TestCardsDesignsettingsByIdFlow:
    @allure.title("POST /Cards -> GET /Cards/{id}/designSettings -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_designsettings_by_id_flow(self, created_card):
        created = created_card

        model = CardDesignsettingsByIdAPI().get_card_designsettings_by_id(created.id)
        assert model.cardID == created.id
        assert model.accountID is not None


    @allure.title("GET /Cards/{id}/designSettings without auth")
    @pytest.mark.ng
    def test_cards_designsettings_by_id_401_without_auth(self, created_card):
        created = created_card

        response = CardDesignsettingsByIdAPI().get_card_designsettings_by_id_without_auth(created.id)
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

