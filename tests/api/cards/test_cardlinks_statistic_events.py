import allure
import pytest
from http import HTTPStatus

from services.cardlinks.cardlink_statistic_download.api_cardlink_statistic_download import (
    CardLinkStatisticDownloadAPI,
)
from services.cardlinks.cardlink_statistic_view.api_cardlink_statistic_view import (
    CardLinkStatisticViewAPI,
)
from services.cards.card_by_id.api_card_by_id import CardByIdAPI
from tests.api.cards.helpers import extract_card_link_id


@allure.epic("API")
@allure.feature("CardLinks")
@pytest.mark.api
@allure.description(
    """
    /cardlinks/{cardLink}/statisticview и /cardlinks/{cardLink}/statisticdownload
    """
)
class TestCardLinksStatisticEvents:
    @allure.title("POST /Cards -> PUT statisticview -> PUT statisticdownload -> DELETE /Cards/{id}")
    @pytest.mark.smoke
    def test_cardlinks_statistic_events_flow(self, created_card):
        created = created_card

        card = CardByIdAPI().get_card_by_id(created.id)
        assert card.url, "Card public url is empty"
        card_link_id = extract_card_link_id(card.url)

        view_response = CardLinkStatisticViewAPI().add_statistic_view(card_link_id)
        assert view_response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

        download_response = CardLinkStatisticDownloadAPI().add_statistic_download(card_link_id)
        assert download_response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)
