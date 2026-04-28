from http import HTTPStatus

import allure

from config.headers import Headers
from services.attributes.attributes_list.endpoints import Endpoints
from services.attributes.attributes_list.models.attributes_list_model import (
    AttributeListItemModel,
    AttributesListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributesListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Attributes")
    def get_attributes(self) -> AttributesListModel:
        response = self._call(
            "GET",
            url=self.endpoints.get_attributes_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict json, got {type(data)}"

        items = {
            str(key): AttributeListItemModel(**value)
            for key, value in data.items()
            if isinstance(value, dict)
        }
        assert items, f"Attributes list is empty or has invalid shape: {data}"
        return AttributesListModel(items=items)

    @allure.step("GET /Attributes without auth")
    def get_attributes_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_attributes_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
