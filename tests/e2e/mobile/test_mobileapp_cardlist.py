import allure
import pytest
from http import HTTPStatus

from src.resources.mobile_api import list_mobile_cards


@allure.epic("Mobile APP")
@allure.feature("Cards")
@allure.title("Cards list")
@pytest.mark.mobile
@pytest.mark.e2e
class TestMobileAppCardList:
    @allure.title("Cards list returns 200 and subscription")
    def test_mobileapp_cards_list_returns_200_and_subscription(self, mobile_api):
        response = list_mobile_cards(mobile_api)

        assert response.status_code == HTTPStatus.OK, (
            f"Cards list failed: {response.status_code}, {response.text}"
        )

        data = response.json()
        assert isinstance(data, list), "Cards list response is not a list"
        assert data, "Cards list returned empty list"
        assert "subscription" in data[0], f"'subscription' not found in first card: {data[0]}"
