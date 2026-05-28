from http import HTTPStatus

import allure

from config.headers import Headers
from services.subscriptions.subscription_designsettings_by_id.endpoints import Endpoints
from services.subscriptions.subscription_designsettings_by_id.models.subscription_designsettings_by_id_model import (
    SubscriptionDesignsettingsByIdModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionDesignsettingsByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Subscriptions/{sub_id}/designsettings")
    def get_subscription_designsettings(self, sub_id: int) -> SubscriptionDesignsettingsByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_designsettings_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        resp_sub_id = data.get("subscriptionID", data.get("SubscriptionID"))
        if resp_sub_id is not None:
            assert int(resp_sub_id) == int(sub_id), (
                f"Expected subscriptionID={sub_id}, got {resp_sub_id}"
            )
        normalized = {
            "subscriptionID": resp_sub_id,
            "accountID": data.get("accountID", data.get("AccountID")),
            "color": data.get("color", data.get("Color")),
            "qrColor": data.get("qrColor", data.get("QrColor")),
            "backgroundColor": data.get("backgroundColor", data.get("BackgroundColor")),
            "foregroundColor": data.get("foregroundColor", data.get("ForegroundColor")),
            "backgroundImagePublicUrl": data.get("backgroundImagePublicUrl", data.get("BackgroundImagePublicUrl")),
            "backgroundAttachmentID": data.get("backgroundAttachmentID", data.get("BackgroundAttachmentID")),
        }
        return SubscriptionDesignsettingsByIdModel(**normalized)

    @allure.step("GET /Subscriptions/{sub_id}/designsettings without auth")
    def get_subscription_designsettings_without_auth(self, sub_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_subscription_designsettings_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
