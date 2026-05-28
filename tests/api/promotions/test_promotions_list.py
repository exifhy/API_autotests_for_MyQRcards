import allure
import pytest
from http import HTTPStatus

from services.promotions.promotions_list.api_promotions_list import PromotionsListAPI


@allure.epic("API")
@allure.feature("Promotions")
@pytest.mark.api
@allure.description(
    """
    /promotions
    """
)
class TestPromotionsList:
    @allure.title("GET /promotions returns list or no content")
    def test_promotions_list_200_or_204(self):
        response, model = PromotionsListAPI().get_promotions()

        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )
        assert isinstance(model.items, list)

        if response.status_code == HTTPStatus.OK and model.items:
            first_item = model.items[0]
            assert first_item.id is None or first_item.id != ""
