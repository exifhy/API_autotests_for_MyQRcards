from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.attributes.attribute_delete_by_id.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AttributeDeleteByIdAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Attributes/{attribute_id}")
    def delete_attribute_by_id(self, attribute_id: int) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_attribute_by_id_endpoint.format(attribute_id=attribute_id),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
            HTTPStatus.NOT_FOUND,
        ), f"Expected 200/202/204/404, got {response.status_code}: {response.text}"
        return response

    @allure.step("DELETE /Attributes/{attribute_id} without auth")
    def delete_attribute_by_id_without_auth(self, attribute_id: int) -> requests.Response:
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_attribute_by_id_endpoint.format(attribute_id=attribute_id),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN), (
            f"Expected 401/403, got {response.status_code}: {response.text}"
        )
        return response
