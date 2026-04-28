import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_request.api_subscription_request import SubscriptionRequestAPI


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    POST /Subscriptions/request  (public, no auth required)
    """
)
class TestSubscriptionRequest:
    @allure.title("POST /Subscriptions/request — random email")
    @pytest.mark.smoke
    def test_subscription_request_200(self):
        response = SubscriptionRequestAPI().create_subscription_request()

        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.CREATED,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        )
