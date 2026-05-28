from http import HTTPStatus

import allure

from config.headers import Headers
from services.accounts.accounts_custom_message_templates.endpoints import Endpoints
from services.accounts.accounts_custom_message_templates.models.accounts_custom_message_templates_model import (
    AccountCustomMessageTemplateModel,
    AccountsCustomMessageTemplatesModel,
)
from src.support.helper import Helper
from src.support.token_utils import get_token


class AccountsCustomMessageTemplatesAPI(Helper):
    def __init__(self):
        self.endpoints = Endpoints()

    @allure.step("GET /Accounts/{account_id}/CustomMessageTemplates")
    def get_accounts_custom_message_templates(self, account_id: int):
        response = self._call(
            "GET",
            url=self.endpoints.get_accounts_custom_message_templates_endpoint.format(account_id=int(account_id)),
            headers=Headers.auth_header(bearer_token=get_token()),
        )
        assert response.status_code in (HTTPStatus.OK, HTTPStatus.NO_CONTENT), (
            f"Expected HTTPStatus.OK/HTTPStatus.NO_CONTENT, got {response.status_code}: {response.text}"
        )
        data = response.json() if response.text else []
        assert isinstance(data, list), f"Expected list, got {type(data)} / {data}"
        items = [AccountCustomMessageTemplateModel(**item) for item in data if isinstance(item, dict)]
        return response, AccountsCustomMessageTemplatesModel(items=items)
