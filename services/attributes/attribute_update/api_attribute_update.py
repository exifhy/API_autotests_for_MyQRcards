from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.attributes.attribute_update.endpoints import Endpoints
from services.attributes.attribute_update.models.attribute_update_model import AttributeUpdateModel
from services.attributes.attribute_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributeUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Attributes")
    def update_attribute(
        self,
        attribute_id: int,
        *,
        payload: list[dict] | None = None,
    ) -> tuple[requests.Response, AttributeUpdateModel]:
        request_payload = payload or Payloads.build_attribute_update_payload(
            attribute_id=attribute_id,
        )
        response = self._call(
            "PUT",
            url=self.endpoints.update_attribute_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected 200/202/204, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        if not data:
            return response, AttributeUpdateModel(id=attribute_id)
        assert isinstance(data, dict), f"Expected dict, got {type(data)} / {data}"
        raw_id = data.get("id") or data.get("ID") or attribute_id
        return response, AttributeUpdateModel(id=int(raw_id))

    @allure.step("PUT /Attributes without auth")
    def update_attribute_without_auth(self, attribute_id: int, *, payload: list[dict] | None = None):
        request_payload = payload or Payloads.build_attribute_update_payload(attribute_id=attribute_id)
        response = self._call(
            "PUT",
            url=self.endpoints.update_attribute_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
