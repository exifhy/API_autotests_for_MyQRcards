import allure
import pytest
from http import HTTPStatus

from services.cards.card_download_by_id.api_card_download_by_id import CardDownloadByIdAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/{id}/download
    """
)
class TestCardsDownloadById:
    @allure.title("POST /Cards -> GET /Cards/{id}/download -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cards_download_by_id_flow(self, created_card):
        created = created_card

        response, model = CardDownloadByIdAPI().get_card_download_by_id(created.id)
        assert response.status_code == HTTPStatus.OK
        assert 'text/vcard' in (model.content_type or '').lower()
        assert model.is_vcard, 'Expected VCARD payload'
        assert model.body_text is not None and 'BEGIN:VCARD' in model.body_text
        assert 'VERSION:3.0' in model.body_text

