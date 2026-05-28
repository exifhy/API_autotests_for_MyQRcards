import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_designsettings_by_id.api_subscription_designsettings_by_id import (
    SubscriptionDesignsettingsByIdAPI,
)


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    /Subscriptions/{subscription_id}/designsettings
    """
)
class TestSubscriptionDesignsettingsById:
    @allure.title("GET /Subscriptions/{subscription_id}/designsettings returns data")
    def test_subscription_designsettings_by_id_200(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        model = SubscriptionDesignsettingsByIdAPI().get_subscription_designsettings(int(sub_id))

        assert model.subscriptionID is None or int(model.subscriptionID) == int(sub_id)

    @allure.title("GET /Subscriptions/{subscription_id}/designsettings without auth")
    @pytest.mark.ng
    def test_subscription_designsettings_by_id_401_without_auth(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        response = SubscriptionDesignsettingsByIdAPI().get_subscription_designsettings_without_auth(int(sub_id))
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)
