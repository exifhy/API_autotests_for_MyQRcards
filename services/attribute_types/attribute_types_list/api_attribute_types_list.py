from http import HTTPStatus

import allure

from config.headers import Headers
from services.attribute_types.attribute_types_list.endpoints import Endpoints
from services.attribute_types.attribute_types_list.models.attribute_types_list_model import (
    AttributeTypeItemModel,
    AttributeTypesListModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributeTypesListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /AttributeTypes")
    def get_attribute_types(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_attribute_types_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code == HTTPStatus.OK, (
            f"Expected HTTPStatus.OK, got {response.status_code}: {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict json, got {type(data)} / {data}"
        items = {
            str(key): AttributeTypeItemModel(**value)
            for key, value in data.items()
            if isinstance(value, dict)
        }
        return response, AttributeTypesListModel(items=items)

    @allure.step("GET /AttributeTypes without auth")
    def get_attribute_types_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_attribute_types_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
