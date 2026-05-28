from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.subscriptions.subscription_contacts_update.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class SubscriptionContactsUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Subscriptions/{sub_id}/contacts")
    def update_subscription_contact(
        self,
        sub_id: int,
        payload: dict,
        *,
        app_id: str | None = None,
    ) -> requests.Response:
        headers = Headers.auth_header(bearer_token=get_token(), app_id=app_id)
        headers["Accept"] = "application/json"
        if app_id:
            headers["X-Aplication-ID"] = str(app_id)

        response = self._call(
            "PUT",
            url=self.endpoints.update_subscription_contacts_endpoint.format(sub_id=int(sub_id)),
            headers=headers,
            json=payload,
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        return response
