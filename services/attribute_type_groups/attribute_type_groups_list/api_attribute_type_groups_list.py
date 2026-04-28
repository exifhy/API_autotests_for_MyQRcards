from http import HTTPStatus

import allure

from config.headers import Headers
from services.attribute_type_groups.attribute_type_groups_list.endpoints import Endpoints
from services.attribute_type_groups.attribute_type_groups_list.models.attribute_type_groups_list_model import (
    AttributeTypeGroupItemModel,
    AttributeTypeGroupsListModel,
)
from services.attribute_type_groups.attribute_type_groups_list.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributeTypeGroupsListAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /AttributeTypeGroups")
    def get_attribute_type_groups(
        self,
        *,
        range_header: str | None = "items=0-199",
        offset: int | None = None,
        fetch: int | None = None,
    ):
        headers = Headers.auth_header(bearer_token=get_token())
        if range_header:
            headers["Range"] = range_header

        response = self._call(
            "GET",
            url=self.endpoints.get_attribute_type_groups_endpoint,
            headers=headers,
            params=Payloads.build_attribute_type_groups_params(offset=offset, fetch=fetch),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT), (
            f"Unexpected status: {response.status_code} {response.text}"
        )

        data = response.json() if response.text else {}
        assert isinstance(data, dict), f"Expected dict json, got {type(data)} / {data}"
        items = {
            str(key): AttributeTypeGroupItemModel(**value)
            for key, value in data.items()
            if isinstance(value, dict)
        }
        return response, AttributeTypeGroupsListModel(items=items)

    @allure.step("GET /AttributeTypeGroups without auth")
    def get_attribute_type_groups_without_auth(self):
        response = self._call(
            "GET",
            url=self.endpoints.get_attribute_type_groups_endpoint,
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected HTTPStatus.UNAUTHORIZED/HTTPStatus.FORBIDDEN, got {response.status_code} {response.text}"
        )
        return response
