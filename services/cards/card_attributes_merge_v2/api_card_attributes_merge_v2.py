from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_attributes_merge_v2.endpoints import Endpoints
from services.cards.card_attributes_merge_v2.models.card_attributes_merge_v2_model import (
    CardAttributeMergeV2ItemModel,
)
from services.cards.card_attributes_merge_v2.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttributesMergeV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Cards/{card_id}/attributes/V2")
    def merge_card_attributes_v2(
        self,
        card_id: int,
        *,
        payload: list[dict] | None = None,
    ) -> tuple[requests.Response, list[CardAttributeMergeV2ItemModel]]:
        request_payload = payload if payload is not None else Payloads.build_card_attributes_v2_payload()
        response = self._call(
            "PUT",
            url=self.endpoints.merge_card_attributes_v2_endpoint.format(card_id=int(card_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected 200/202/204, got {response.status_code}: {response.text}"
        )
        items = [CardAttributeMergeV2ItemModel(**item) for item in response.json()] if response.text else []
        return response, items

    @allure.step("PUT /Cards/{card_id}/attributes/V2 (raw, no assert — for negative cases)")
    def merge_card_attributes_v2_raw(self, card_id, payload) -> requests.Response:
        return self._call(
            "PUT",
            url=self.endpoints.merge_card_attributes_v2_endpoint.format(card_id=card_id),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )

    @allure.step("PUT /Cards/{card_id}/attributes/V2 (raw body, no JSON encoding — for null-body case)")
    def merge_card_attributes_v2_raw_body(self, card_id, raw_body: str) -> requests.Response:
        headers = Headers.auth_header(bearer_token=get_token())
        return self._call(
            "PUT",
            url=self.endpoints.merge_card_attributes_v2_endpoint.format(card_id=card_id),
            headers=headers,
            data=raw_body,
        )

    @allure.step("PUT /Cards/{card_id}/attributes/V2 without auth")
    def merge_card_attributes_v2_without_auth(self, card_id: int) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.merge_card_attributes_v2_endpoint.format(card_id=int(card_id)),
            headers=Headers.without_authorization_field_header(),
            json=Payloads.build_card_attributes_v2_payload(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
