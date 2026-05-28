from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_designsettings_merge.endpoints import Endpoints
from services.subscriptions.subscription_designsettings_merge.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionDesignsettingsMergeAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Subscriptions/{sub_id}/designsettings")
    def merge_subscription_designsettings(
        self,
        sub_id: int,
        *,
        color: str | None = None,
        qr_color: str | None = None,
        background_color: str | None = None,
        foreground_color: str | None = None,
        payload: dict | None = None,
    ) -> tuple[requests.Response, dict]:
        request_payload = payload or Payloads.build_subscription_designsettings_merge_payload(
            color=color,
            qr_color=qr_color,
            background_color=background_color,
            foreground_color=foreground_color,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.merge_subscription_designsettings_endpoint.format(sub_id=int(sub_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        return response, request_payload
