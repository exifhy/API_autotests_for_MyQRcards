import allure
import pytest
from http import HTTPStatus

from services.cardlinks.cardlink_download_v2.api_cardlink_download_v2 import CardLinkDownloadV2API
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardLinks/{cardLink}/card/download/V2
    """
)
class TestCardLinksDownloadV2:
    @allure.title("POST /Cards -> GET /cardLinks/{cardLink}/card/download/V2 -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_download_v2_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        response, model = CardLinkDownloadV2API().get_cardlink_download_v2(card_link_id)
        assert response.status_code == HTTPStatus.OK
        assert "text/vcard" in (model.content_type or "").lower()
        assert model.is_vcard, "Expected VCARD payload"
        assert model.body_text is not None and "BEGIN:VCARD" in model.body_text
        assert "VERSION:3.0" in model.body_text
