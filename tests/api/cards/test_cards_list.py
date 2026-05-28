import allure
import pytest
from http import HTTPStatus

from services.cards.cards_list.api_cards_list import CardsListAPI
from services.cards.cards_list_v2.api_cards_list_v2 import CardsListV2API


@allure.epic("API")
@allure.feature("Cards")
@pytest.mark.api
@allure.description(
    """
    Проверки списков /Cards и /Cards/v2.0.
    """
)
class TestCardsList:
    @allure.title("GET /Cards returns cards list")
    @pytest.mark.smoke
    def test_cards_list_200_or_206(self):
        response, model = CardsListAPI().get_cards(range_header='items=0-199')
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get('Content-Range') or response.headers.get('content-range')
            assert content_range
        assert isinstance(model.items, list)
        assert model.items, 'Cards list is empty'
        assert model.items[0].id is not None
        assert model.items[0].subscription is not None

    @allure.title("GET /Cards supports offset/fetch query")
    def test_cards_list_with_paging_query(self):
        response, model = CardsListAPI().get_cards(range_header=None, offset=0, fetch=5)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Cards without auth")
    @pytest.mark.ng
    def test_cards_list_401_without_auth(self):
        response = CardsListAPI().get_cards_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)

    @allure.title("GET /Cards/v2.0 returns cards list")
    @pytest.mark.smoke
    def test_cards_list_v2_200_or_206(self):
        response, model = CardsListV2API().get_cards_v2(range_header='items=0-199', all_data=True)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        if response.status_code == HTTPStatus.PARTIAL_CONTENT:
            content_range = response.headers.get('Content-Range') or response.headers.get('content-range')
            assert content_range
        assert isinstance(model.items, list)
        assert model.items, 'Cards v2 list is empty'
        assert model.items[0].id is not None
        assert model.items[0].subscription is not None

    @allure.title("GET /Cards/v2.0 supports offset/fetch and AllData query")
    def test_cards_list_v2_with_paging_query(self):
        response, model = CardsListV2API().get_cards_v2(range_header=None, offset=0, fetch=5, all_data=True)
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT)
        assert isinstance(model.items, list)

    @allure.title("GET /Cards/v2.0 without auth")
    @pytest.mark.ng
    def test_cards_list_v2_401_without_auth(self):
        response = CardsListV2API().get_cards_v2_without_auth()
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
