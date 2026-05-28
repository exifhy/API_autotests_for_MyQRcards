from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_custom_message_templates_delete.endpoints import Endpoints
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCustomMessageTemplatesDeleteAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("DELETE /Accounts/{account_id}/CustomMessageTemplates")
    def delete_accounts_custom_message_templates(self, account_id: int, template_ids: list[int]):
        response = self._call(
            "DELETE",
            url=self.endpoints.delete_accounts_custom_message_templates_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=template_ids,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response
