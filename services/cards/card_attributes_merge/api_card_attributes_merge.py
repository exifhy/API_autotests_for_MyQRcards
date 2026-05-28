from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_attributes_merge.endpoints import Endpoints
from services.cards.card_attributes_merge.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttributesMergeAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /cards/{card_id}/attributes")
    def merge_card_attributes(
        self,
        card_id: int,
        *,
        payload: list[dict] | None = None,
    ) -> requests.Response:
        request_payload = payload or Payloads.build_card_attributes_merge_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.merge_card_attributes_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected 200/202/204, got {response.status_code}: {response.text}"
        )
        return response

    @allure.step("PUT /cards/{card_id}/attributes without auth")
    def merge_card_attributes_without_auth(self, card_id: int) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.merge_card_attributes_endpoint.format(card_id=int(card_id)),
            headers=Headers.without_authorization_field_header(),
            json=Payloads.build_card_attributes_merge_payload(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
