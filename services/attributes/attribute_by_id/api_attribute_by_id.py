from http import HTTPStatus

import allure

from config.headers import Headers
from services.attributes.attribute_by_id.endpoints import Endpoints
from services.attributes.attribute_by_id.models.attribute_by_id_model import (
    AttributeByIdModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributeByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Attributes/{attribute_id}")
    def get_attribute_by_id(self, attribute_id: int) -> AttributeByIdModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_attribute_by_id_endpoint.format(attribute_id=attribute_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict json, got {type(data)}"
        assert "attribute" in data, f"'attribute' missing in response: {data}"
        assert "type" in data, f"'type' missing in response: {data}"
        assert int(data["attribute"]["id"]) == int(attribute_id), (
            f"Expected attribute.id={attribute_id}, got {data['attribute'].get('id')}"
        )
        return AttributeByIdModel(**data)

    @allure.step("GET /Attributes/{attribute_id} without auth")
    def get_attribute_by_id_without_auth(self, attribute_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_attribute_by_id_endpoint.format(attribute_id=attribute_id),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
