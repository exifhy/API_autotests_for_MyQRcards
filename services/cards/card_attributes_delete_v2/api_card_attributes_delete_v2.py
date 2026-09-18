from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.cards.card_attributes_delete_v2.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class CardAttributesDeleteV2API(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Cards/{card_id}/attributes/V2/{card_attribute_node_id}")
    def delete_card_attribute_v2(self, card_id: int, card_attribute_node_id: int) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_card_attribute_v2_endpoint.format(
                card_id=int(card_id), card_attribute_node_id=int(card_attribute_node_id)
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected 200/202/204, got {response.status_code}: {response.text}"
        )
        return response

    @allure.step("DELETE /Cards/{card_id}/attributes/V2/{card_attribute_node_id} (raw, no assert)")
    def delete_card_attribute_v2_raw(self, card_id, card_attribute_node_id) -> requests.Response:
        return self._call(
            "DELETE",
            url=self.endpoints.delete_card_attribute_v2_endpoint.format(
                card_id=card_id, card_attribute_node_id=card_attribute_node_id
            ),
            headers=Headers.auth_header(bearer_token=get_token()),
        )

    @allure.step("DELETE /Cards/{card_id}/attributes/V2/{card_attribute_node_id} without auth")
    def delete_card_attribute_v2_without_auth(self, card_id: int, card_attribute_node_id: int) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_card_attribute_v2_endpoint.format(
                card_id=int(card_id), card_attribute_node_id=int(card_attribute_node_id)
            ),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
