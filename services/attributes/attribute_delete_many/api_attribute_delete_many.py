from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.attributes.attribute_delete_many.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributeDeleteManyAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Attributes")
    def delete_attributes(self, attribute_ids: list[int]) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_attributes_endpoint,
            headers=Headers.auth_header(bearer_token=get_token()),
            json=[int(aid) for aid in attribute_ids],
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), f"Expected 200/202/204/404, got {response.status_code}: {response.text}"
        return response

    @allure.step("DELETE /Attributes without auth")
    def delete_attributes_without_auth(self, attribute_ids: list[int]) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_attributes_endpoint,
            headers=Headers.without_authorization_field_header(),
            json=[int(aid) for aid in attribute_ids],
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
