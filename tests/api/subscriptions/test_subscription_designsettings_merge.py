import allure
import pytest
from http import HTTPStatus

from services.subscriptions.subscription_designsettings_by_id.api_subscription_designsettings_by_id import (
    SubscriptionDesignsettingsByIdAPI,
)
from services.subscriptions.subscription_designsettings_merge.api_subscription_designsettings_merge import (
    SubscriptionDesignsettingsMergeAPI,
)


@allure.epic("API")
@allure.feature("Subscriptions")
@pytest.mark.api
@allure.description(
    """
    PUT /Subscriptions/{subscription_id}/designsettings
    GET /Subscriptions/{subscription_id}/designsettings
    """
)
class TestSubscriptionDesignsettingsMerge:
    @allure.title("PUT /Subscriptions/{subscription_id}/designsettings updates color and GET returns it")
    def test_subscription_designsettings_merge_color_flow(self, cfg):
        sub_id = cfg.get("subscription_id")
        assert sub_id, "cfg['subscription_id'] is empty"

        before = SubscriptionDesignsettingsByIdAPI().get_subscription_designsettings(int(sub_id))
        original_color = before.color
        test_color = "112233"

        try:
            response, payload = SubscriptionDesignsettingsMergeAPI().merge_subscription_designsettings(
                int(sub_id),
                color=test_color,
            )
            assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT)

            after = SubscriptionDesignsettingsByIdAPI().get_subscription_designsettings(int(sub_id))
            assert after.subscriptionID is None or int(after.subscriptionID) == int(sub_id)
            assert after.color == payload["color"]
        finally:
            restore_payload = {}
            if original_color:
                restore_payload["color"] = original_color
            else:
                restore_payload["color"] = test_color
            SubscriptionDesignsettingsMergeAPI().merge_subscription_designsettings(
                int(sub_id),
                payload=restore_payload,
            )
