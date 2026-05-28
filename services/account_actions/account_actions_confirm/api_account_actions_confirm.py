from http import HTTPStatus

import allure
import requests

from config.headers import Headers
from services.account_actions.account_actions_confirm.endpoints import Endpoints
from src.support.helper import Helper


class AccountActionsConfirmAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /accountActions/{guid}")
    def confirm_account_action(self, guid: str) -> requests.Response:
        response = self._call(
            "PUT",
            url=self.endpoints.confirm_account_action_endpoint.format(guid=str(guid)),
            headers=Headers.without_authorization_field_header(),
        )
        assert response.status_code in (
            HTTPStatus.OK,
            HTTPStatus.ACCEPTED,
            HTTPStatus.NO_CONTENT,
        ), f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        return response
