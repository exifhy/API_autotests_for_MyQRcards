from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_custom_message_templates_update.endpoints import Endpoints
from services.accounts.accounts_custom_message_templates_update.payloads import Payloads
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCustomMessageTemplatesUpdateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("PUT /Accounts/{account_id}/CustomMessageTemplates")
    def update_accounts_custom_message_template(self, account_id: int, template_id: int):
        payload = Payloads.build_accounts_custom_message_template_update_payload(template_id=template_id)
        response = self._call(
            "PUT",
            url=self.endpoints.update_accounts_custom_message_templates_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.ACCEPTED/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        return response, payload
