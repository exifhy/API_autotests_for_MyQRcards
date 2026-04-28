import allure
import pytest
from http import HTTPStatus

from services.cards.cards_lastupdate.api_cards_lastupdate import CardsLastUpdateAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/lastupdate
    """
)
class TestCardsLastUpdate:
    @allure.title("GET /Cards/lastupdate returns change list")
    @pytest.mark.smoke
    def test_cards_lastupdate_200_or_206(self):
        response, model = CardsLastUpdateAPI().get_cards_lastupdate(range_header='items=0-199')
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get('Content-Range') or response.headers.get('content-range')
            assert content_range
        assert isinstance(model.items, list)
        assert model.items, 'Cards lastupdate list is empty'
        assert model.items[0].accountID is not None
        assert model.items[0].cardID is not None
        assert model.items[0].lastModified is not None

    @allure.title("GET /Cards/lastupdate supports offset/fetch query")
    def test_cards_lastupdate_with_paging_query(self):
        response, model = CardsLastUpdateAPI().get_cards_lastupdate(range_header=None, offset=0, fetch=5)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Cards/lastupdate without auth")
    @pytest.mark.ng
    def test_cards_lastupdate_401_without_auth(self):
        response = CardsLastUpdateAPI().get_cards_lastupdate_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
