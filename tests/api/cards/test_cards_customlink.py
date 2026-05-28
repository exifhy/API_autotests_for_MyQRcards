import allure
import pytest
from http import HTTPStatus

from services.cards.cards_customlink.api_cards_customlink import CardsCustomLinkAPI


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    /Cards/customlink
    """
)
class TestCardsCustomLink:
    @allure.title("GET /Cards/customlink returns custom links list")
    @pytest.mark.smoke
    def test_cards_customlink_200_or_206(self):
        response, model = CardsCustomLinkAPI().get_cards_customlink(range_header='items=0-199')
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get('Content-Range') or response.headers.get('content-range')
            assert content_range
        assert isinstance(model.items, list)
        assert model.items, 'Cards customlink list is empty'
        assert model.items[0].id is not None
        assert model.items[0].name is None or model.items[0].name != ''

    @allure.title("GET /Cards/customlink supports offset/fetch query")
    def test_cards_customlink_with_paging_query(self):
        response, model = CardsCustomLinkAPI().get_cards_customlink(range_header=None, offset=0, fetch=5)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Cards/customlink without auth")
    @pytest.mark.ng
    def test_cards_customlink_401_without_auth(self):
        response = CardsCustomLinkAPI().get_cards_customlink_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
