import allure
import pytest
from http import HTTPStatus

from services.cardlinks.cardlink_download.api_cardlink_download import CardLinkDownloadAPI
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardLinks/{cardLink}/card/download
    """
)
class TestCardLinksDownload:
    @allure.title("POST /Cards -> GET /cardLinks/{cardLink}/card/download -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_download_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkDownloadAPI().get_cardlink_download(card_link_id)
        assert response.status_code == HTTPStatus.OK
        assert "text/vcard" in (model.content_type or "").lower()
        assert model.is_vcard, "Expected VCARD payload"
        assert model.body_text is not None and "BEGIN:VCARD" in model.body_text
        assert "VERSION:3.0" in model.body_text
