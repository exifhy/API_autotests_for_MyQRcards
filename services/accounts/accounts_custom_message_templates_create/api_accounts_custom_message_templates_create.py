from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_custom_message_templates_create.endpoints import Endpoints
from services.accounts.accounts_custom_message_templates_create.payloads import Payloads
from services.accounts.accounts_custom_message_templates.models.accounts_custom_message_templates_model import (
    AccountCustomMessageTemplateModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCustomMessageTemplatesCreateAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("POST /Accounts/{account_id}/CustomMessageTemplates")
    def create_accounts_custom_message_template(self, account_id: int):
        payload = Payloads.build_accounts_custom_message_template_payload()
        response = self._call(
            "POST",
            url=self.endpoints.create_accounts_custom_message_templates_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
            json=payload,
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED), (
            f"Expected HTTPStatus.OK/HTTPStatus.CREATED, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else {}
        model = AccountCustomMessageTemplateModel(**data)
        return response, model, payload
