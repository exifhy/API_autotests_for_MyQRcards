from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.attribute_types.attribute_types_list.api_attribute_types_list import AttributeTypesListAPI
from services.attributes.attribute_create.endpoints import Endpoints
from services.attributes.attribute_create.models.attribute_create_model import AttributeCreateModel
from services.attributes.attribute_create.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


def _first_attribute_type_id() -> int:
    _, model = AttributeTypesListAPI().get_attribute_types()
    assert model.items, "AttributeTypes list is empty — cannot create attribute"
    return int(next(iter(model.items)))


class AttributeCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Attributes")
    def create_attribute(
        self,
        attribute_type_id: int | None = None,
        *,
        payload: list[dict] | None = None,
    ) -> tuple[requests.Response, AttributeCreateModel]:
        request_payload = payload or Payloads.build_attribute_create_payload(
            attribute_type_id=attribute_type_id or _first_attribute_type_id()
        )
        response = self._call(
            "POST",
            url=self.endpoints.create_attribute_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED), (
            f"Expected 200/201/202, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        if isinstance(data, list):
            assert data, f"Empty list in response: {response.text}"
            item = data[0]
        else:
            item = data
        assert isinstance(item, dict), f"Expected dict item, got {type(item)} / {item}"
        raw_id = item.get("id") or item.get("ID") or item.get("attributeID") or item.get("AttributeID")
        assert raw_id, f"No attribute id in response: {data}"
        return response, AttributeCreateModel(id=int(raw_id))

    @allure.step("POST /Attributes without auth")
    def create_attribute_without_auth(self, payload: list[dict] | None = None):
        request_payload = payload or Payloads.build_attribute_create_payload()
        response = self._call(
            "POST",
            url=self.endpoints.create_attribute_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=request_payload,
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
